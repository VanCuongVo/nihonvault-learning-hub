from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.auth_service import AuthService
from app.repositories.unit_of_work import UnitOfWork


def get_auth_service() -> AuthService:
    return AuthService(uow_factory=UnitOfWork)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency: Cung cấp AsyncSession cho mỗi request.
    - Mở session khi request bắt đầu.
    - Tự động rollback nếu xảy ra exception.
    - Luôn luôn đóng session sau khi request hoàn thành để giải phóng connection về pool.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
