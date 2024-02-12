from enum import Enum, unique

from pydantic import UUID4
from pydantic_core import ValidationError

from postgrest.exceptions import APIError
from supabase._async.client import AsyncClient

from app.controller.base import BaseController
from app.schemas.response import ControllerResponse
from app.utils import MultipleResponse, SingleResponse
from app.schemas.categories import (
    CategoryOut,
    CategoryInDB,
    CategoryFilter,
    CategorySave,
)

Category = SingleResponse[CategoryInDB]
Categories = MultipleResponse[CategoryInDB]

_Return = ControllerResponse[CategoryOut | list[CategoryOut] | None]

class _CategoriesController(
    BaseController[
        CategorySave,
        _Return,
        CategoryFilter
    ]):

    @unique
    class QueriesEnum(Enum):
        """Queries to perform in postgres api syntax"""
        ALL = '*'

    _queries = QueriesEnum

    def __init__(self, *args, **kwarg) -> None:
        self._table = 'categories'
        super().__init__(args, kwarg)

    async def save(self, client: AsyncClient, model: CategorySave) -> _Return:
        response = ControllerResponse()
        response_db = None
        try:
            response_db: Categories = await client.table(self._table)\
                .insert(
                    model.model_dump(
                        mode='json',
                        exclude_none=True),
                    count='exact')\
                .execute()
        except (APIError, ValidationError) as error:
            # TODO: Change to logging
            if isinstance(error, APIError):
                print('Error at the DB API request')
                print(error.details)
                print(error.message)
            else:
                print('Validation Error at cats data from DB')
                print(error.errors())
            response.success = False
            return response

        if not response_db.data:
            response.success = False
            return response

        try:
            model_out = CategoryOut.model_validate(response_db.data[0], from_attributes=True)
            response.count = response_db.count
            response.data = model_out
        except ValidationError as error:
            print(f'Validation error, total of errors {error.error_count()}')
            print(error.errors())
            response.success= False
        return response

    async def update(self, client: AsyncClient, model: CategorySave) -> _Return:
        response = ControllerResponse()
        response_db = None
        try:
            response_db: Categories = await client.table(self._table)\
                .update(
                    model.model_dump(mode='json', exclude=['id']),
                    count='exact')\
                .eq('id', model.id)\
                .execute()
        except (APIError, ValidationError) as error:
            # TODO: Change to logging
            if isinstance(error, APIError):
                print('Error at the DB API request')
                print(error.details)
                print(error.message)
            else:
                print('Validation Error at cats data from DB')
                print(error.errors())
            response.success = False
            return response

        if not response_db.data:
            response.success = False
            return response

        try:
            model_out = CategoryOut.model_validate(response_db.data[0], from_attributes=True)
            response.count = response_db.count
            response.data = model_out
        except ValidationError as error:
            print(f'Validation error, total of errors {error.error_count()}')
            print(error.errors())
            response.success= False
        return response

    async def select(self, client: AsyncClient, params: CategoryFilter) -> _Return:
        response = ControllerResponse()
        response_db = None
        last_element = params.page * params.limit
        final_element = (params.page + 1) * params.limit
        try:
            query = client.table(self._table)\
                .select(_CategoriesController._queries.ALL.value, count='exact')\
                .range(last_element, final_element)

            if params.name:
                query.like('name', f'%{params.name}%')
            response_db: Categories = await query.execute()
        except (APIError, ValidationError) as error:
            # TODO: Change to logging
            if isinstance(error, APIError):
                print('Error at the DB API request')
                print(error.details)
                print(error.message)
            else:
                print('Validation Error at cats data from DB')
                print(error.errors())
            response.success = False
            return response

        if not response_db.count:
            response.success = False
            return response

        try:
            response.data = [
                CategoryOut.model_validate(record, from_attributes=True)
                for record in response_db.data
            ]
            response.count = response_db.count
        except ValidationError as error:
            print(f'Validation error, total of errors {error.error_count()}')
            print(error.errors())
            response.success= False
        return response

    async def unique(self, client: AsyncClient, model_id: UUID4) -> _Return:
        response = ControllerResponse()
        response_db = None
        try:
            response_db: Category = await client.table(self._table)\
                .select(
                    _CategoriesController._queries.ALL.value,
                    count='exact')\
                .eq('id', model_id)\
                .single()\
                .execute()
        except (APIError, ValidationError) as error:
            # TODO: Change to logging
            if isinstance(error, APIError):
                print('Error at the DB API request')
                print(error.details)
                print(error.message)
            else:
                print('Validation Error at cats data from DB')
                print(error.errors())
            response.success = False
            return response

        if not response_db.count:
            response.success = False
            return response

        try:
            model_out = CategoryOut.model_validate(response_db.data, from_attributes=True)
            response.count = 1
            response.data = model_out
        except ValidationError as error:
            print(f'Validation error, total of errors {error.error_count()}')
            print(error.errors())
            response.success= False
        return response

    async def delete(self, client: AsyncClient, model_id: UUID4) -> _Return:
        response = ControllerResponse()
        try:
            response_db: Categories = await client.table(self._table)\
                .delete(count='exact')\
                .eq('id', model_id)\
                .execute()
            response.count = response_db.count
        except APIError as error:
            # TODO: Change to logging
            print('Error at the DB API request')
            print(error.details)
            print(error.message)
            response.success = False
            return response
        return response
