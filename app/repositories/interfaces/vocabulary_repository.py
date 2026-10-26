from abc import abstractmethod
from app.enums.JLPTLevel import JLPTLevel
from app.enums.PartOfSpeech import PartOfSpeech
from app.models.vocabulary import Vocabulary
from app.repositories.interfaces.repository import IRepository


class IVocabularyRepository(IRepository[Vocabulary]):

    @abstractmethod
    async def get_by_word(self, word: str) -> Vocabulary | None:
        pass

    @abstractmethod
    async def get_existing_words(self, words: list[str]) -> set[str]:
        """Lấy danh sách các từ đã có trong DB để check trùng lặp hàng loạt."""
        pass

    @abstractmethod
    async def bulk_add(self, vocabularies: list[Vocabulary]) -> list[Vocabulary]:
        """Thêm hàng loạt từ vựng cùng lúc để tối ưu hiệu năng."""
        pass
    
    @abstractmethod
    async def get_paginated(self, skip: int = 0, limit: int = 20, search: str | None = None, jlpt_level: JLPTLevel | None = None, part_of_speech: PartOfSpeech | None = None) -> tuple[list[Vocabulary], int]:
        pass
    
    
    