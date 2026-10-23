from abc import abstractmethod
from app.models.user import User
from app.repositories.interfaces.repository import IRepository


class IAuthRepository(IRepository[User]):

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass
        
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass