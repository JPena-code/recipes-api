from fastapi import status
from fastapi import APIRouter, Request

from app.core.deps.auth import LoginForm, RefreshTokenForm, HTTPCredentials

from app.schemas.auth import Token
from app.schemas.response import Response
from app.controller.auth import _AuthController
from app.utils.exceptions.common import unauthenticated, server_error


AuthController = _AuthController()
ResponseType = Response[Token]

router = APIRouter()


@router.post(
    '/login',
    response_model=ResponseType,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    response_description='Authenticate user with email and password',)
async def login(request: Request, form_data: LoginForm):
    controller_response = await AuthController.login(form_data)
    if not controller_response.success:
        raise unauthenticated(request)

    response = ResponseType(
        data=controller_response.data,
        message='Logged successfully',
        resource_type='Tokens',
        path=request.url.path)

    return response


@router.post(
    '/token/refresh',
    response_model=ResponseType,
    response_model_exclude_none=True,
)
async def refresh(
    request: Request,
    token: HTTPCredentials,
    refresh_token: RefreshTokenForm
    ):
    controller_response = await AuthController.refresh_token(refresh_token, token)
    if not controller_response.success:
        raise server_error(request, 'Internal server error, cannot refresh token')

    response = ResponseType(
        data=controller_response.data,
        message='Tokens refreshed',
        resource_type='Tokens',
        path=request.url.path)

    return response
