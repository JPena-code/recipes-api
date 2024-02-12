from enum import  IntEnum, auto
from typing import Generic, TypeVar

from fastapi import status

from pydantic import Field
from pydantic import BaseModel, ConfigDict
from pydantic import PositiveInt, StrictBool, NonNegativeInt


Resource = TypeVar('Resource', BaseModel, list[BaseModel], dict, list[dict])

class Errors(IntEnum):
    """Possible errors returner by controllers"""
    NO_RETURN = auto()
    ACTION = auto()
    VALIDATION = auto()
    UNAUTHENTICATED = auto()
    UNAUTHORIZED = auto()


class Response(BaseModel, Generic[Resource]):
    """API Body Response"""
    model_config = ConfigDict(
        frozen=True,
        title='Response Schema',
        description='Response schema to standard behavior of the API',
    )

    status: PositiveInt = Field(
        default=status.HTTP_200_OK,
        ge=status.HTTP_100_CONTINUE,
        le=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
    message: str = 'Success response'
    data: Resource | None = None
    resource_type: str | None = 'Error'
    count: NonNegativeInt | None = None
    path: str
    next: str | None = None

class ControllerResponse(BaseModel, Generic[Resource]):
    """Controllers response to retrieve to routers"""
    model_config = ConfigDict(
        validate_assignment=True,
        title='Response schema for controllers',
        description='Response schema to standard behavior of the API',
    )
    success: StrictBool = True
    data: Resource | None = None
    count: NonNegativeInt = 0
    error: Errors | None = None




__all__ = [
    'Errors',
    'Response',
    'ControllerResponse',
]
