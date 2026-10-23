import pydantic
import typing

T = typing.TypeVar("T")

class APIResponse(pydantic.BaseModel, typing.Generic[T]):
    success: bool
    message: str
    data: T | None = None