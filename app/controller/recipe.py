from enum import Enum, unique

from pydantic import UUID4
from pydantic_core import ValidationError

from postgrest.exceptions import APIError
from supabase._async.client import AsyncClient

from app.logging import logger
from app.controller.base import BaseController
from app.schemas.response import ControllerResponse
from app.utils import MultipleResponse, SingleResponse
from app.schemas.recipes import (
    RecipeOut,
    RecipeInDB,
    RecipeSave,
    RecipeFilter
)

Recipe = SingleResponse[RecipeInDB]
Recipes = MultipleResponse[list[RecipeInDB]]

_Return = ControllerResponse[RecipeOut | list[RecipeOut] | None]

class _RecipesController(
    BaseController[
        RecipeSave,
        _Return,
        RecipeFilter
    ]):

    @unique
    class Queries(Enum):
        """Queries to perform in postgres api syntax"""
        INFO = '*'

    _queries = Queries

    def __init__(self, *args, **kwargs):
        self._table = 'recipes'
        self._rcp_insert = 'insert_recipe'
        self._view = 'recipes_full'
        super().__init__(args, kwargs)

    async def save(self, client: AsyncClient, model: RecipeSave) -> _Return:
        response = ControllerResponse[RecipeOut]()
        try:
            response_db: Recipe = await client.rpc(self._rcp_insert, {
                'recipe_json': model.model_dump(mode='json')
            }).execute()
        except (APIError, ValidationError) as error:
            if isinstance(error, APIError):
                logger.error(
                    'Error at the DB API request "%s - %s"',
                    error.code,
                    error.message
                )
            else:
                logger.debug(
                    'Validation Error at cats data from DB "%s" total "%d"',
                    error.title,
                    error.error_count()
                )
            response.success = False
            return response
        if not response_db.data:
            response.success = False
            return response
        response.data = RecipeOut.model_validate(response_db.data, from_attributes=True)
        return response

    async def update(self, client: AsyncClient, model: RecipeSave) -> _Return:
        # TODO: Make the store procedure to update a recipe
        # Also call it here, search if supabase sanitize the input data
        raise NotImplementedError('Update Recipe not implemented yet')

    async def select(self, client: AsyncClient,  params: RecipeFilter) -> _Return:
        response = ControllerResponse[list[RecipeOut]]()
        response_db = None
        last_element = params.page * params.limit
        final_element = (params.page + 1) * params.limit
        try:
            query = client.table(self._view)\
                .select(_RecipesController._queries.INFO.value, count='exact')\
                .range(last_element, final_element)

            if params.category:
                query.eq('category_id', params.category)
            if params.title:
                query.like('title', f'%{params.title}%')
            # TODO: extract id from list of json objects
            # if params.tag:
            #     query.eq('tags.id', params.tag)
            response_db: Recipes = await query.execute()
        except (APIError, ValidationError) as error:
            if isinstance(error, APIError):
                logger.error(
                    'Error at the DB API request "%s - %s"',
                    error.code,
                    error.message
                )
            else:
                logger.debug(
                    'Validation Error at cats data from DB "%s" total "%d"',
                    error.title,
                    error.error_count()
                )
            response.success = False
            return response

        if not response_db.count:
            response.success = False
            return response
        try:
            response.data = [
                RecipeOut.model_validate(record, from_attributes=True)
                for record in response_db.data
            ]
            response.count = response_db.count
        except ValidationError as error:
            logger.debug(
                'Validation Error "%s" total "%d"',
                error.title,
                error.error_count()
            )
            response.success= False
        return response

    async def unique(self, client: AsyncClient, model_id: UUID4) -> _Return:
        response = ControllerResponse[RecipeOut]()
        response_db = None
        try:
            response_db: Recipe = await client.table(self._view)\
                .select(_RecipesController._queries.INFO.value, count='exact')\
                .eq('id', model_id)\
                .single()\
                .execute()
            if not response.count:
                return None
        except (APIError, ValidationError) as error:
            if isinstance(error, APIError):
                logger.error(
                    'Error at the DB API request "%s - %s"',
                    error.code,
                    error.message
                )
            else:
                logger.debug(
                    'Validation Error at cats data from DB "%s" total "%d"',
                    error.title,
                    error.error_count()
                )
            response.success = False
            return response

        if not response_db.count:
            response.success = False
            return response

        try:
            model_out = RecipeOut.model_validate(response_db.data, from_attributes=True)
            response.count = 1
            response.data = model_out
        except ValidationError as error:
            logger.debug(
                'Validation Error "%s" total "%d"',
                error.title,
                error.error_count()
            )
            response.success= False
        return response

    async def delete(self, client: AsyncClient, model_id: UUID4) -> _Return:
        response = ControllerResponse()
        try:
            response_db: Recipes = await client.table(self._table)\
                .delete(count='exact')\
                .eq('id', model_id)\
                .execute()
            response.count = response_db.count
        except APIError as error:
            logger.error(
                'Error at the DB API request "%s - %s"',
                error.code,
                error.message
            )
            response.success = False
            return response
        return response
