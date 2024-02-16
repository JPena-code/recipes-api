from collections.abc import AsyncGenerator

from jwt import ExpiredSignatureError

from pydantic import UUID4
from postgrest.exceptions import APIError
from supabase._async.client import AsyncClient

from gotrue import AuthResponse
from gotrue.errors import AuthApiError

from app.db import Repository
from app.logging import logger
from app.schemas.auth import Token, TokenPayload
from app.schemas.response import ControllerResponse
from app.core.deps.auth import LoginForm, HTTPCredentials, RefreshTokenForm


# TODO: Handle exceptions in Authentication
def current_user(auth: HTTPCredentials) -> UUID4 | None:
    if auth is None:
        return None
    user = None
    token = auth.credentials
    try:
        payload: TokenPayload = TokenPayload.decode_token(token)
        user = payload.sub
    except ExpiredSignatureError:
        pass
    return user

class _AuthController:
    """_AuthController
        Controller of the request related with the authentication process
        of an User
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._repo = Repository

    async def auth_client(self, auth: HTTPCredentials) -> AsyncGenerator[AsyncClient, None, None]:
        if auth is None:
            yield None
        token = auth.credentials
        if not current_user(auth):
            yield None
        client = None
        try:
            client = await self._repo.get_client()
            client._auth_token = {
                "apiKey": client.supabase_key,
                "Authorization": f"Bearer {token}",
            }
            yield client
        except APIError as error:
            logger.error(
                'Cannot set Supabase auth client "%s - %s"',
                error.code,
                error.message,)
        finally:
            if client:
                await client.postgrest.aclose()
                await client.storage.aclose()
                await client.auth.close()

    async def no_auth(self) -> AsyncClient:
        return await self._repo.get_client()

    async def refresh_token(
            self,
            form_refresh: RefreshTokenForm,
            http_credentials: HTTPCredentials=None) -> ControllerResponse[Token | None]:
        token = None
        if http_credentials:
            token = http_credentials.credentials
        response: ControllerResponse[Token] = ControllerResponse()
        new_token: Token = None
        if token:
            try:
                payload: TokenPayload = TokenPayload.decode_token(token)
                new_token = Token(
                    access_token=token,
                    refresh_token=form_refresh.refresh_token,
                    expires_at=payload.exp,
                    token_type='bearer')
            except ExpiredSignatureError:
                pass
        if new_token is None and response.success:
            try:
                response_db: AuthResponse = await self._repo.admin.auth.refresh_session(form_refresh.refresh_token)
                new_token = Token.model_validate(response_db.session, from_attributes=True)
            except AuthApiError as error:
                logger.error(
                    'Cannot set Supabase auth client "%s - %s"',
                    error.status,
                    error.message,)
                response.success = False
        response.data = new_token
        return response

    async def login(self, data: LoginForm) -> ControllerResponse[Token | None]:
        response = ControllerResponse[Token]()
        try:
            client: AsyncClient  = await self._repo.get_client()
            sign_in: AuthResponse = await client.auth.sign_in_with_password(
                {
                    'email': data.email,
                    'password': data.password
                }
            )
            response.data = Token.model_validate(sign_in.session, from_attributes=True)
        except AuthApiError as error:
            logger.error(
                'Cannot set Supabase auth client "%s - %s"',
                error.status,
                error.message,)
            response.success = False
        return response
