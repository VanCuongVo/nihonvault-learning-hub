from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base
from app.repositories.interfaces.repository import IRepository

T = TypeVar("T", bound=Base)


class GenericRepository(IRepository[T], Generic[T]):
    
    # self là đối tượng hiện tại giống vs this 
    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model 

    async def get_by_id(self, entity_id: int) -> T | None:
        return await self.db.get(self.model, entity_id)

    async def get_all(self) -> list[T]:
        statement = select(self.model)
        result = await self.db.scalars(statement)
        return list(result.all())

    async def add(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def update(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def delete(self, entity: T) -> None:
        await self.db.delete(entity)
        await self.db.flush()