from abc import ABC, abstractmethod
from fastapi import UploadFile

from app.enums.PartOfSpeech import PartOfSpeech
from app.enums.JLPTLevel import JLPTLevel
from app.schemas.vocabulary import PaginatedVocabularyResponse, VocabularyCreateRequest, VocabularyImportResult, VocabularyResponse, VocabularyUpdateRequest


class IVocabularyService(ABC):
    @abstractmethod
    async def import_from_csv(self, file: UploadFile, user_id: int) -> VocabularyImportResult:
        pass
    
    @abstractmethod
    async def create(self, request: VocabularyCreateRequest, user_id: int) -> VocabularyResponse:
        pass
    
    @abstractmethod
    async def get_by_id(self, vocab_id: int) -> VocabularyResponse:
        pass
    
    @abstractmethod
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        jlpt_level: JLPTLevel | None = None,
        part_of_speech: PartOfSpeech | None = None,
    ) -> PaginatedVocabularyResponse:
        pass
    
    @abstractmethod
    async def update(self, vocab_id: int, request: VocabularyUpdateRequest) -> VocabularyResponse:
        pass
    
    @abstractmethod
    async def delete(self, vocab_id: int) -> None:
        pass