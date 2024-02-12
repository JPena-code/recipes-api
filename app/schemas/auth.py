import time
import inspect
from functools import lru_cache
from typing_extensions import TypedDict

import jwt
from fastapi import status
from fastapi import Request, HTTPException, Form

from pydantic import BaseModel, ValidationError, Field
from pydantic import PositiveInt, HttpUrl, UUID4, EmailStr

from app.utils.exceptions.common import unprocessed_entity
from app.core.settings import settings


@lru_cache(maxsize=None, typed=True)
def form_body(cls: type[BaseModel]):
    form_params = []
    for name, field in cls.model_fields.items():
        # TODO: Metadata arguments are being ignored
        # Is required to use the field.metadata list to recover
        form_params.append(
            inspect.Parameter(
                name,
                inspect.Parameter.POSITIONAL_ONLY,
                annotation=field.annotation,
                default=Form(
                    field.default if not field.default else ...,
                    description=field.description,
                    alias=field.alias,
                    max_length=getattr(field, 'max_length', None),
                    min_length=getattr(field, 'min_length', None),
                    title=getattr(field, 'title', None),
                    json_schema_extra=field.json_schema_extra,
                )
            )
        )

    async def _as_form(request: Request, **data) -> cls:
        try:
            return cls.model_validate(data)
        except ValidationError as error:
            errors = [
                {
                    'type': _error['type'],
                    'loc': '-> '.join([str(loc) for loc in _error['loc']]).strip(),
                    'msg': _error['msg']
                } for _error in error.errors()
            ]
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=unprocessed_entity(
                    request,
                    data=errors,
                    msg='Unprocessed entity Form-urlencoded'
                )
            ) from error

    signature = inspect.signature(_as_form)
    form_params.append(signature.parameters['request'])
    signature = signature.replace(parameters=form_params)
    _as_form.__signature__ = signature

    return _as_form

class Login(BaseModel):
    email: EmailStr
    password: str


class RefreshToken(BaseModel):
    """Refresh token payload from request url form"""
    refresh_token: str = Field(
        description='Refresh token issued by the server',
    )
    grant_type: str = Field(
        description='Type of request token',
        examples=['refresh_token'],
        pattern='refresh_token$'
    )

    @classmethod
    def as_from(cls):
        return form_body(cls)


class AppMetaData(TypedDict):
    """Supabase metadata info
        provider: current provider used to signing the user
        providers: list of user available providers
    """
    provider: str
    providers: list[str]


class AMR(BaseModel):
    """Authentication methods used by the user"""
    method: str
    timestamp: int


class Token(BaseModel):
    """Access token model for the user"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: int


class TokenPayload(BaseModel):
    """Token payload recovered from the token signed by supabase
       Also it could be use to self sign the token
    """
    aud: str = Field(
        description='Audience (who or what the token is intended for)'
    )
    exp: PositiveInt = Field(
        default_factory=lambda : int(time.time()) + settings.EXPIRATION_TIME,
        description='Expiration Time (seconds since Unix epoch)'
    )
    iat: PositiveInt = Field(
        default_factory=time.time,
        description='Issued at (seconds since Unix epoch)'
    )
    iss: HttpUrl = Field(
        default='http://localhost/login', # Server issuer
        description='Issuer (who create and sign this token)'
    )
    sub: UUID4 = Field(
        description='Subject (who the token refers)'
    )
    email: EmailStr
    phone: str
    app_metadata: AppMetaData
    user_metadata: dict = Field(
        description='Additional information about the users'
    )
    role: str
    aal: str = Field(
        description='Level of multi-factor authentication'
    )
    amr: list[AMR]
    session_id: UUID4

    @classmethod
    def decode_token(cls, token: str):
        payload = jwt.decode(
            token,
            key=settings.SECRET.get_secret_value(),
            audience=['authenticated'],
            algorithms=[settings.ALGORITHM]
        )
        return cls.model_validate(payload)
