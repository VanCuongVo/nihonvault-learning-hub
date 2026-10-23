from abc import ABC, abstractmethod
from types import TracebackType
from app.repositories.interfaces.auth_repository import IAuthRepository


class IUnitOfWork(ABC):

    @property
    @abstractmethod
    def users(self) -> IAuthRepository:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool | None:
        pass