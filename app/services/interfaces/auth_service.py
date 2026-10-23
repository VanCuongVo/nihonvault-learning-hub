from abc import ABC, abstractmethod
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
)


class IAuthService(ABC):

    @abstractmethod
    async def register(self, request: RegisterRequest) -> UserResponse:
        pass

    @abstractmethod
    async def login(self, request: LoginRequest) -> TokenResponse:
        pass