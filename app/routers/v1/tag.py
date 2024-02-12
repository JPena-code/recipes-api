from typing import Annotated

from fastapi import status, Depends
from fastapi import APIRouter, Request

from app.utils import PathID
from app.controller import TagsController
from app.core.deps import Anon, Client, User
from app.schemas.response import Errors, Response
from app.schemas.tags import (
    TagIn,
    TagOut,
    TagFilter,
    TagSave
)
from app.utils.exceptions.common import (
    not_found,
    server_error,
    expired_token,
    unauthenticated
)


Responses = Response[list[TagOut] | TagOut | dict]

router = APIRouter()

@router.get(
    '/',
    name='All Tags',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Get all tags available')
async def tags(
        request: Request,
        client: Anon,
        tag_query: Annotated[TagFilter, Depends()]=None
    ):
    """GET Tags
        Create an item with all the information:

        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
        \f
        :param request: request from client
        :param client: DB session client
        :param tag_query: tag fields to filter.
    """
    # Indexing pages at zero in server
    next_params = tag_query.model_copy(update={'page': tag_query.page + 1})
    tag_query.page -= 1

    response = await TagsController.select(client, tag_query)
    if not response.success:
        raise server_error(
            request,
            'Internal error retrieving tags resources',
        )

    return Response[list[TagOut]](
        count=response.count,
        data=response.data,
        resource_type='Tag',
        path=request.url.path,
        next=request.url.path + request.url.replace_query_params(
            **next_params.model_dump(mode='json', exclude_none=True, exclude_defaults=True)
        ).query
    )


@router.get(
    '/{model_id:uuid}',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Get tag filter by its UUID')
async def tag(
        request: Request,
        client: Anon,
        model_id: PathID
    ):
    response = await TagsController.unique(client, model_id)

    if response.error == Errors.NO_RETURN:
        raise not_found(
            request,
            f'Resource with id: {model_id}. Not found',
        )

    if not response.success:
        raise server_error(
            request,
            'Internal error retrieving tag',
        )

    return Response[TagOut](
        data=response.data,
        resource_type='Tag',
        count=response.count,
        path=request.url.path
    )


@router.post(
    '/',
    response_model=Responses,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    description='Save a new tag resource')
async def save(
        request: Request,
        user: User,
        client: Client,
        new_tag: TagIn
    ):
    if not user:
        raise unauthenticated(request)

    tag_save = TagSave(
        **new_tag.model_dump(mode='python'),
    )

    response = await TagsController.save(client, tag_save)

    if not response.success:
        raise server_error(
            request,
            'Internal error storing resource',
        )

    return Response[TagOut](
        status=status.HTTP_201_CREATED,
        data=response.data,
        resource_type='Tag',
        path=request.url.path,
        count=response.count
    )


@router.patch(
    '/{model_id:uuid}',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Update a tag resource')
async def update(
        request: Request,
        user: User,
        client: Client,
        model_id: PathID,
        tag_in: TagIn
    ):
    if not user:
        raise unauthenticated(request)

    tag_update = TagSave(
        **{
            'id': model_id,
            **tag_in.model_dump(mode='python')
        }
    )

    response = await TagsController.update(client, tag_update)
    if not response.success:
        raise server_error(
            request,
            f'Internal error updating resource with id: {model_id}',
        )

    return Response[TagOut](
        status=status.HTTP_200_OK,
        data=response.data,
        resource_type='Tag',
        path=request.url.path,
        count=response.count
    )


@router.delete(
    '/{model_id:uuid}',
    response_model=Responses,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    description='Delete a tag resource')
async def delete(
        request: Request,
        user: User,
        client: Client,
        model_id: PathID,
    ):
    if not user:
        raise unauthenticated(request)

    response = await TagsController.delete(client, model_id)
    if not response.success:
        raise server_error(
            request,
            f'Internal error updating resource with id: {model_id}',
        )

    return Response(
        status=status.HTTP_200_OK,
        message='Resource delete successfully',
        resource_type='Tag',
        count=response.count,
        path=request.url.path)
