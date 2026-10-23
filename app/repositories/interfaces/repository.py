from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from app.core.database import Base

T = TypeVar("T", bound=Base)

class IRepository(ABC, Generic[T]):

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[T]:
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, entity: T) -> None:
        pass