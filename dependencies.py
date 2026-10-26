from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.vocabulary_service import VocabularyService
from app.core.database import AsyncSessionLocal
from app.services.auth_service import AuthService
from app.core.jwt_manager import JWTManager
from app.repositories.unit_of_work import UnitOfWork
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import jwt

security = HTTPBearer()

def get_auth_service() -> AuthService:
    return AuthService(uow_factory=UnitOfWork)

def get_vocab_service() -> VocabularyService:
    return VocabularyService(uow_factory=UnitOfWork)


# 2. Dependency xác thực token và trích xuất thông tin User
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Tự động trích xuất chuỗi token từ header Authorization: Bearer <token>
    và giải mã để lấy thông tin user_id, email, role.
    """
    token = credentials.credentials
    try:
        payload = JWTManager.decode_token(token, expected_type="access")
        return {
            "id": int(payload["sub"]),
            "email": payload["email"],
            "role": payload["role"],
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn, vui lòng đăng nhập lại",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
