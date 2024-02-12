from typing import Annotated

from fastapi import status, Depends
from fastapi import APIRouter, Request

from app.utils import PathID
from app.core.deps import Anon, Client, User
from app.controller import CategoriesController
from app.schemas.response import Errors, Response
from app.schemas.categories import (
    CategoryIn,
    CategoryOut,
    CategoryFilter,
    CategorySave
)
from app.utils.exceptions.common import (
    not_found,
    server_error,
    expired_token,
    unauthenticated,
)

Responses = Response[list[CategoryOut] | CategoryOut | None]

router = APIRouter()

@router.get(
    '/',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Get all categories available')
async def categories(
        request: Request,
        client: Anon,
        category_query: Annotated[CategoryFilter, Depends()]=None
    ):
    # Indexing pages at zero in server
    next_params = category_query.model_copy(update={'page': category_query.page + 1})
    category_query.page -= 1

    response = await CategoriesController.select(client, category_query)
    if not response.success:
        raise server_error(
            request,
            'Internal error retrieving categories resources')

    return Response[list[CategoryOut]](
        count=response.count,
        data=response.data,
        resource_type='Category',
        path=request.url.path,
        next=request.url.path + request.url.replace_query_params(
            **next_params.model_dump(mode='json', exclude_none=True, exclude_defaults=True)
        ).query
    )


@router.get(
    '/{model_id:uuid}',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Get category filter by its UUID')
async def category(
        request: Request,
        client: Anon,
        model_id: PathID
    ):
    response = await CategoriesController.unique(client, model_id)

    if response.error == Errors.NO_RETURN:
        raise not_found(
            request,
            f'Resource with id: {model_id}. Not found'
        )

    if not response.success:
        raise server_error(
            request,
            'Error retrieving Category',
        )

    return Response[CategoryOut](
        data=response.data,
        resource_type='Category',
        count=response.count,
        path=request.url.path
    )


@router.post(
    '/',
    response_model=Responses,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    description='Save a new category resource')
async def save(
        request: Request,
        user: User,
        client: Client,
        new_category: CategoryIn
    ):
    if not user:
        raise unauthenticated(request)

    category_save = CategorySave(
        **new_category.model_dump(mode='python')
    )

    response = await CategoriesController.save(client, category_save)

    if not response.success:
        raise server_error(
            request,
            'Error storing resource',
        )

    return Response[CategoryOut](
        status=status.HTTP_201_CREATED,
        data=response.data,
        resource_type='Category',
        path=request.url.path,
        count=response.count
    )


@router.patch(
    '/{model_id:uuid}',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Update a category resource')
async def update(
        request: Request,
        user: User,
        client: Client,
        model_id: PathID,
        category_in: CategoryIn
    ):
    if not user:
        raise unauthenticated(request)

    category_update = CategorySave.model_validate(
        {
            'id': model_id,
            **category_in.model_dump(mode='python')
        }
    )

    response = await CategoriesController.update(client, category_update)
    if not response.success:
        raise server_error(
            request,
            f'Error updating resource with id: {model_id}',
        )

    return Response[CategoryOut](
        status=status.HTTP_200_OK,
        data=response.data,
        resource_type='Category',
        path=request.url.path,
        count=response.count
    )


@router.delete(
    '/{model_id:uuid}',
    response_model=Responses,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    description='Delete a category resource')
async def delete(
        request: Request,
        user: User,
        client: Client,
        model_id: PathID
    ):
    if not user:
        raise unauthenticated(request)

    response = await CategoriesController.delete(client, model_id)
    if not response.success:
        raise server_error(
            request,
            f'Error updating resource with id: {model_id}',
        )

    return Response(
        status=status.HTTP_200_OK,
        message='Resource delete successfully',
        resource_type='Category',
        count=response.count,
        path=request.url.path)
