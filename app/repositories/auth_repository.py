from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.interfaces.auth_repository import IAuthRepository
from app.repositories.base_repository import GenericRepository


class AuthRepository(GenericRepository[User], IAuthRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
    
    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.db.scalars(statement)
        return result.first()

    async def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await self.db.scalars(statement)
        return result.first()
    
    
