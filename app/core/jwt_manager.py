import os
from datetime import datetime, timedelta, timezone
from typing import Literal
import jwt
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    # JWT configuration
    secret_key: str = ""
    algorithm: str = "HS256"

    # Token expiration configuration
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JWT_",
        extra="ignore",
    )

settings = JWTSettings()


class JWTManager:

    @staticmethod
    def _create_token(
        user_id: int,
        email: str,
        role: str,
        token_type: Literal["access", "refresh"],
        expires_delta: timedelta,
    ) -> str:
        if not settings.secret_key:
            raise RuntimeError("JWT_SECRET_KEY chưa được cấu hình")

        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "type": token_type,
            "iat": now,
            "exp": now + expires_delta,
        }

        return jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.algorithm,
        )

    @staticmethod
    def create_access_token(
        user_id: int,
        email: str,
        role: str,
    ) -> str:
        return JWTManager._create_token(
            user_id=user_id,
            email=email,
            role=role,
            token_type="access",
            expires_delta=timedelta(
                minutes=settings.access_token_expire_minutes
            ),
        )

    @staticmethod
    def create_refresh_token(
        user_id: int,
        email: str,
        role: str,
    ) -> str:
        return JWTManager._create_token(
            user_id=user_id,
            email=email,
            role=role,
            token_type="refresh",
            expires_delta=timedelta(
                days=settings.refresh_token_expire_days
            ),
        )

    @staticmethod
    def decode_token(
        token: str,
        expected_type: Literal["access", "refresh"],
    ) -> dict:
        if not settings.secret_key:
            raise RuntimeError("JWT_SECRET_KEY chưa được cấu hình")

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["sub", "iat", "exp", "type"]},
        )

        if payload.get("type") != expected_type:
            raise jwt.InvalidTokenError("Sai loại token")

        return payload
