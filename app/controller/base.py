import inspect
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, UUID4
from supabase._async.client import AsyncClient

_SaveT = TypeVar('_SaveT', bound=BaseModel)
_Return = TypeVar('_Return', bound=BaseModel)
_Params = TypeVar('_Params', bound=BaseModel)

class BaseController(
    ABC,
    Generic[_SaveT, _Return, _Params]):
    """Abstract class to inherit to it for the models controllers"""

    _instance = None

    def __new__(cls, *args, **Kwargs):
        if cls._instance is None:
            coroutine_parent = inspect.getmembers(BaseController, predicate=inspect.iscoroutinefunction)
            for coroutine in coroutine_parent:
                child_method = getattr(cls, coroutine[0])
                if not inspect.iscoroutinefunction(child_method):
                    raise RuntimeError(
                        f'Method "{child_method.__name__}" must be a coroutine')
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """ init method, must include least the db client"""

    @abstractmethod
    async def save(self, client: AsyncClient, model: _SaveT) -> _Return:
        """save
            Abstract method for the base controller
        """

    @abstractmethod
    async def update(self, client: AsyncClient, model: _SaveT) -> _Return:
        """update
            Abstract method for the base controller
        """

    @abstractmethod
    async def select(self, client: AsyncClient, params: _Params) -> _Return:
        """select
            Abstract method for the base controller
        """

    @abstractmethod
    async def unique(self, client: AsyncClient, model_id: UUID4) -> _Return:
        """unique
            Abstract method for the base controller
        """

    @abstractmethod
    async def delete(self, client: AsyncClient, model_id: UUID4) -> _Return:
        """delete
            Abstract method for the base controller
        """

__all__ = [
    'BaseController',
]
