from fastapi import APIRouter, HTTPException, status, Depends

from dependencies import get_auth_service
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService
from app.schemas.api_response import APIResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
# auth_service = AuthService()
@router.post(
    "/register",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def register(request: RegisterRequest,
                   service: AuthService = Depends(get_auth_service)
                   ) -> UserResponse:
    try:
        result = await service.register(request)
        return APIResponse[TokenResponse](
                    success=True,
                    message="Đăng ký thành công",
                    data=result,
                )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
)
async def login(request: LoginRequest,
                service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        result =  await service.login(request)
        return APIResponse[TokenResponse](
            success=True,
            message="Đăng nhập thành công",
            data=result,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )