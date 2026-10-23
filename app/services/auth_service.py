from collections.abc import Callable
from datetime import datetime, timedelta, timezone
import os
import jwt
from app.services.interfaces.auth_service import IAuthService
from app.repositories.interfaces.unit_of_work import IUnitOfWork
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
)
from app.models.user import User
from app.validators.password_hash import PasswordHasher
from app.core.jwt_manager import JWTManager

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "nihonvault_default_secret_key_change_me")
ALGORITHM = "HS256"


class AuthService(IAuthService):

    def __init__(self, uow_factory: Callable[[], IUnitOfWork] = UnitOfWork):
        self.uow_factory = uow_factory

    async def register(self, request: RegisterRequest) -> UserResponse:
        email = str(request.email).strip().lower()
        username = request.username.strip()

        async with self.uow_factory() as uow:
            existing_email = await uow.users.get_by_email(email)
            if existing_email:
                raise ValueError("Email đã được sử dụng")

            existing_username = await uow.users.get_by_username(username)
            if existing_username:
                raise ValueError("Tên người dùng (username) đã được sử dụng")

            user = User(
                email=email,
                username=username,
                hashed_password=PasswordHasher.hash_password(request.password),
                full_name=request.full_name,
            )

            await uow.users.add(user)
            await uow.commit()

            role_val = (
                user.role.value if hasattr(user.role, "value") else str(user.role)
            )

            return UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                role=role_val,
            )

    async def login(self, request: LoginRequest) -> TokenResponse:
        email = str(request.email).strip().lower()

        async with self.uow_factory() as uow:
            user = await uow.users.get_by_email(email)

            if user is None or not PasswordHasher.verify_password(
                request.password, user.hashed_password
            ):
                raise ValueError("Email hoặc mật khẩu không đúng")

            now = datetime.now(timezone.utc)
            role_val = (
                user.role.value if hasattr(user.role, "value") else str(user.role)
            )
            access_token = JWTManager.create_access_token(
                user_id=user.id,
                email=user.email,
                role=role_val,
            )
            refresh_token = JWTManager.create_refresh_token(
                user_id=user.id,
                email=user.email,
                role=role_val,
            )
            return TokenResponse(
                access_token=access_token,
                refresh_token = refresh_token,
                token_type="bearer",
                user={
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": role_val,
                },
            )
