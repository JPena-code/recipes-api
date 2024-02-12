from typing import Annotated

from fastapi import status, Depends, Body
from fastapi import APIRouter, Request, UploadFile

from app.utils import PathID, ImageFile
from app.controller import RecipesController
from app.core.deps import Anon, Client, User
from app.schemas.response import Errors, Response
from app.schemas.recipes import (
    RecipeIn,
    RecipeOut,
    RecipeSave,
    RecipeFilter,
)
from app.utils.exceptions.common import (
    not_found,
    server_error,
    expired_token,
    unauthenticated
)


# TODO: Make real save uploaded files
def fake_save(file: UploadFile):
    print('Fake saving...')
    return f'http://localhost:8000/{file.filename}'

Responses = Response[list[RecipeOut] | RecipeOut | dict]

router = APIRouter()

@router.get(
    '/',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Get all recipes available',)
async def recipes(
        request: Request,
        client: Anon,
        recipe_query: Annotated[RecipeFilter, Depends()]=None
    ):
    # Indexing pages at zero in server
    next_params = recipe_query.model_copy(update={'page': recipe_query.page + 1})
    recipe_query.page -= 1

    response = await RecipesController.select(client, recipe_query)
    if not response.success:
        raise server_error(
            request,
            'Error retrieving recipes resources',
        )

    return Response[list[RecipeOut]](
        count=response.count,
        data=response.data,
        resource_type='Recipe',
        path=request.url.path,
        next=request.url.path + request.url.replace_query_params(
            **next_params.model_dump(mode='json', exclude_defaults=True, exclude_none=True)
        ).query
    )


@router.get(
    '/{model_id:uuid}',
    response_model=Responses,
    response_model_exclude_none=True,
    description='Get recipe filter by its UUID')
async def recipe(
        request: Request,
        client: Anon,
        model_id: PathID
    ):
    response = await RecipesController.unique(client, model_id)

    if response.error == Errors.NO_RETURN:
        raise not_found(
            request,
            f'Resource with id: {model_id}. Not found',
        )

    if not response.success:
        raise server_error(
            request,
            'Internal error retrieving recipe',
        )

    return Response[RecipeOut](
        data=response.data,
        resource_type='Recipe',
        count=response.count,
        path=request.url.path
    )


@router.post(
    '/',
    response_model=Responses,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    description='Save a new recipe resource')
async def save(
        request: Request,
        user: User,
        client: Client,
        image: ImageFile=None,
        recipe_new: RecipeIn=Body(description='Recipe information content'),
    ):
    if not user:
        raise unauthenticated(request)
    url_image = None
    if image:
        url_image = fake_save(image)
    recipe_save = RecipeSave.model_validate(
        {
            'image': url_image,
            'user_id': user,
            **recipe_new.model_dump(mode='python'),
        }
    )
    response = await RecipesController.save(client, recipe_save)

    if not response.success:
        raise server_error(
            request,
            'Internal error storing resource',
        )

    return Response[RecipeOut](
        status=status.HTTP_201_CREATED,
        data=response.data,
        resource_type='Recipe',
        path=request.url.path,
    )


@router.patch(
    '/{model_id:uuid}',
    response_model=Responses,
    status_code=status.HTTP_202_ACCEPTED,
    description='Update a Recipe resource')
async def update(
        request: Request,
        user: User,
        client: Client,
        model_id: PathID,
        recipe_in: RecipeIn
    ):
    # TODO: modify to recive new image
    if not user:
        raise unauthenticated(request)

    recipe_update = RecipeSave(
        **{
            'id': model_id,
            **recipe_in.model_dump(mode='python')
        }
    )

    response = await RecipesController.update(client, recipe_update)
    if not response.success:
        raise server_error(
            request,
            f'Internal error updating resource with id: {model_id}',
        )

    return Response[RecipeOut](
        status=status.HTTP_200_OK,
        data=response.data,
        resource_type='Recipe',
        path=request.url.path,
        count=response.count
    )


@router.delete(
    '/{model_id:uuid}',
    status_code=status.HTTP_200_OK,
    response_model=Responses,
    description='Delete a recipe resource')
async def delete(
        request: Request,
        user: User,
        client: Client,
        model_id: PathID
    ):
    if not user:
        raise unauthenticated(request)

    response = await RecipesController.delete(client, model_id)
    if not response.success:
        raise server_error(
            request,
            f'Internal error updating resource with id: {model_id}',
        )

    return Response(
        status=status.HTTP_200_OK,
        message='Resource delete successfully',
        resource_type='Recipe',
        count=response.count,
        path=request.url.path)
