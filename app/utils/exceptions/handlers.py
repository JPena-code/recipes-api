from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .common import unprocessed_entity

def validation_error(request: Request, exc: RequestValidationError):
    error_content = [
        {
            'type': error['type'],
            'loc': '-> '.join([str(loc) for loc in error['loc']]).strip(),
            'msg': error['msg']
        } for error in exc.errors()
    ]
    return JSONResponse(
        content=unprocessed_entity(
            request,
            msg='Unprocessable JSON object',
            data=error_content
        ),
        media_type='application/json',
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
