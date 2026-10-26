from collections.abc import Callable
from fastapi import UploadFile
from app.models.vocabulary import Vocabulary
from app.repositories.interfaces.unit_of_work import IUnitOfWork
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.vocabulary import (
    VocabularyCreateRequest,
    VocabularyUpdateRequest,
    VocabularyResponse,
    PaginatedVocabularyResponse,
    VocabularyImportResult,
)
from app.enums.JLPTLevel import JLPTLevel
from app.enums.PartOfSpeech import PartOfSpeech
from app.services.importers.vocab_importer import VocabCSVImporter
from app.services.importers.vocab_excel_importer import VocabExcelImporter


class VocabularyService:

    def __init__(self, uow_factory: Callable[[], IUnitOfWork] = UnitOfWork):
        self.uow_factory = uow_factory

    # 1. Tạo 1 từ đơn lẻ
    async def create(self, request: VocabularyCreateRequest, user_id: int) -> VocabularyResponse:
        word = request.word.strip()
        async with self.uow_factory() as uow:
            existing = await uow.vocabularies.get_by_word(word)
            if existing:
                raise ValueError(f"Từ vựng '{word}' đã tồn tại trong hệ thống")

            vocab = Vocabulary(
                word=word,
                reading=request.reading.strip(),
                meaning_vi=request.meaning_vi.strip(),
                part_of_speech=request.part_of_speech,
                jlpt_level=request.jlpt_level,
                romaji=request.romaji.strip() if request.romaji else None,
                han_viet=request.han_viet.strip() if request.han_viet else None,
                audio_url=request.audio_url,
                created_by_id=user_id,
            )
            await uow.vocabularies.add(vocab)
            await uow.commit()
            return VocabularyResponse.model_validate(vocab)

    # 2. Xem chi tiết theo ID
    async def get_by_id(self, vocab_id: int) -> VocabularyResponse:
        async with self.uow_factory() as uow:
            vocab = await uow.vocabularies.get_by_id(vocab_id)
            if not vocab:
                raise LookupError("Không tìm thấy từ vựng")
            return VocabularyResponse.model_validate(vocab)

    # 3. Lấy danh sách có phân trang & tìm kiếm
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        jlpt_level: JLPTLevel | None = None,
        part_of_speech: PartOfSpeech | None = None,
    ) -> PaginatedVocabularyResponse:
        skip = (page - 1) * page_size
        async with self.uow_factory() as uow:
            items, total = await uow.vocabularies.get_paginated(
                skip=skip,
                limit=page_size,
                search=search,
                jlpt_level=jlpt_level,
                part_of_speech=part_of_speech,
            )
            return PaginatedVocabularyResponse(
                total=total,
                page=page,
                page_size=page_size,
                items=[VocabularyResponse.model_validate(i) for i in items],
            )

    # 4. Chỉnh sửa từ vựng
    async def update(self, vocab_id: int, request: VocabularyUpdateRequest) -> VocabularyResponse:
        async with self.uow_factory() as uow:
            vocab = await uow.vocabularies.get_by_id(vocab_id)
            if not vocab:
                raise LookupError("Không tìm thấy từ vựng")

            # Cập nhật các trường được truyền lên (bỏ qua các trường None)
            update_data = request.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(vocab, field, value)

            await uow.vocabularies.update(vocab)
            await uow.commit()
            return VocabularyResponse.model_validate(vocab)

    # 5. Xóa từ vựng
    async def delete(self, vocab_id: int) -> None:
        async with self.uow_factory() as uow:
            vocab = await uow.vocabularies.get_by_id(vocab_id)
            if not vocab:
                raise LookupError("Không tìm thấy từ vựng")

            await uow.vocabularies.delete(vocab)
            await uow.commit()

    # 6. Import từ File (CSV / Excel)
    async def import_from_file(self, file: UploadFile, user_id: int) -> VocabularyImportResult:
        filename = file.filename.lower()
        if filename.endswith(".xlsx"):
            valid_rows, errors = await VocabExcelImporter.parse_excel(file)
        elif filename.endswith(".csv"):
            valid_rows, errors = await VocabCSVImporter.parse_csv(file)
        else:
            raise ValueError("Chỉ chấp nhận file .xlsx hoặc .csv")

        words_to_check = [r.word for r in valid_rows]

        async with self.uow_factory() as uow:
            existing_words = await uow.vocabularies.get_existing_words(words_to_check)
            vocab_entities: list[Vocabulary] = []
            seen_in_file = set()

            for row in valid_rows:
                if row.word in existing_words:
                    errors.append({"word": row.word, "error": "Từ vựng đã có trong DB"})
                    continue
                if row.word in seen_in_file:
                    errors.append({"word": row.word, "error": "Từ vựng bị lặp lại trong file"})
                    continue

                seen_in_file.add(row.word)
                vocab_entities.append(
                    Vocabulary(
                        word=row.word,
                        reading=row.reading,
                        meaning_vi=row.meaning_vi,
                        part_of_speech=row.part_of_speech,
                        jlpt_level=row.jlpt_level,
                        romaji=row.romaji,
                        han_viet=row.han_viet,
                        audio_url=row.audio_url,
                        created_by_id=user_id,
                    )
                )

            if vocab_entities:
                await uow.vocabularies.bulk_add(vocab_entities)
                await uow.commit()

            success_count = len(vocab_entities)
            failed_count = len(errors)
            total_rows = success_count + failed_count

            return VocabularyImportResult(
                total_rows=total_rows,
                success_count=success_count,
                failed_count=failed_count,
                errors=errors,
            )