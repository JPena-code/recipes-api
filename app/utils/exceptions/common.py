from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, Request, status

from app.schemas.response import Response

COMMON_HEADERS = {
    'Content-Type': 'application/json'
}

UNAUTHORIZED_HEADERS = {
    **COMMON_HEADERS,
    'WWW-Authenticate': 'Bearer',
}


def not_found(request: Request, msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=json_error(
            status=status.HTTP_404_NOT_FOUND,
            message=msg,
            path=request.url.path,
            resource_type='Server error'
        ),
        headers=COMMON_HEADERS
    )


def server_error(request: Request, msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=json_error(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=msg,
            path=request.url.path,
            resource_type='Server error'
        ),
        headers=COMMON_HEADERS
    )


def unauthenticated(request: Request) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=json_error(
            status=status.HTTP_401_UNAUTHORIZED,
            message='Cannot authenticate user, invalid credentials',
            path=request.url.path,
            resource_type='Unauthenticated error'
        ),
        headers=UNAUTHORIZED_HEADERS
    )


def expired_token(request: Request, expired_at) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=json_error(
            status=status.HTTP_401_UNAUTHORIZED,
            message=f'Token expired at {expired_at}, refresh token',
            path=request.url.path,
            resource_type='Token expired'
        ),
        headers=UNAUTHORIZED_HEADERS
    )


def unprocessed_entity(request: Request, msg: str, data):
    return json_error(
        data=data,
        message=msg,
        path=request.url.path,
        resource_type='Validation error',
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        count=len(data) if hasattr(data, '__len__') else None,
    )


def json_error(**kwargs):
    """json_error

        Encode in JSON format a Response object that correspond
        to an error message
        \f
        :param kwargs: arguments to create a Response object
    """
    resource_type = None
    if (data := kwargs.get('data', None)):
        resource_type = type(data)
        if list == resource_type:
            resource_type = list[type(data[0])]
    return jsonable_encoder(
        Response[resource_type](**kwargs),
        exclude_none=True
    )
