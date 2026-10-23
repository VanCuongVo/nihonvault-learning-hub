from types import TracebackType
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.repositories.interfaces.unit_of_work import IUnitOfWork
from app.repositories.interfaces.auth_repository import IAuthRepository
from app.repositories.auth_repository import AuthRepository


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.db: AsyncSession | None = None
        self._users: IAuthRepository | None = None

    @property
    def users(self) -> IAuthRepository:
        if self._users is None:
            raise RuntimeError("UnitOfWork chưa được khởi tạo (phải dùng 'async with')")
        return self._users

    async def __aenter__(self) -> "UnitOfWork":
        self.db = AsyncSessionLocal()
        self._users = AuthRepository(self.db)
        return self

    async def commit(self) -> None:
        if self.db is None:
            raise RuntimeError("UnitOfWork chưa được khởi tạo")
        await self.db.commit()

    async def rollback(self) -> None:
        if self.db is not None:
            await self.db.rollback()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            if self.db is not None:
                await self.db.close()
            self.db = None
            self._users = None

        return False