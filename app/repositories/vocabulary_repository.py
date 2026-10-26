from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vocabulary import Vocabulary
from app.enums.JLPTLevel import JLPTLevel
from app.enums.PartOfSpeech import PartOfSpeech
from app.repositories.interfaces.vocabulary_repository import IVocabularyRepository
from app.repositories.base_repository import GenericRepository


class VocabularyRepository(GenericRepository[Vocabulary], IVocabularyRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Vocabulary)

    async def get_by_word(self, word: str) -> Vocabulary | None:
        stmt = select(Vocabulary).where(Vocabulary.word == word)
        res = await self.db.scalars(stmt)
        return res.first()

    async def get_existing_words(self, words: list[str]) -> set[str]:
        if not words:
            return set()
        stmt = select(Vocabulary.word).where(Vocabulary.word.in_(words))
        res = await self.db.scalars(stmt)
        return set(res.all())

    async def bulk_add(self, vocabularies: list[Vocabulary]) -> list[Vocabulary]:
        self.db.add_all(vocabularies)
        await self.db.flush()
        return vocabularies

    # HÀM MỚI: Phân trang + Tìm kiếm + Lọc
    async def get_paginated(
        self,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        jlpt_level: JLPTLevel | None = None,
        part_of_speech: PartOfSpeech | None = None,
    ) -> tuple[list[Vocabulary], int]:
        stmt = select(Vocabulary)

        # Lọc theo cấp độ
        if jlpt_level:
            stmt = stmt.where(Vocabulary.jlpt_level == jlpt_level)
        # Lọc theo từ loại
        if part_of_speech:
            stmt = stmt.where(Vocabulary.part_of_speech == part_of_speech)
        # Tìm kiếm theo từ, cách đọc hoặc nghĩa tiếng Việt
        if search:
            search_pattern = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    Vocabulary.word.ilike(search_pattern),
                    Vocabulary.reading.ilike(search_pattern),
                    Vocabulary.meaning_vi.ilike(search_pattern),
                    Vocabulary.han_viet.ilike(search_pattern),
                )
            )

        # Đếm tổng số bản ghi khớp điều kiện
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.scalar(count_stmt)) or 0

        # Lấy dữ liệu theo phân trang
        stmt = stmt.order_by(Vocabulary.id.desc()).offset(skip).limit(limit)
        items = list((await self.db.scalars(stmt)).all())

        return items, total