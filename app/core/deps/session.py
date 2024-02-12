from typing import Annotated

from pydantic import UUID4
from fastapi import Depends

from supabase._async.client import AsyncClient

from app.controller.auth import _AuthController, current_user

AuthController = _AuthController()

Anon = Annotated[AsyncClient, Depends(AuthController.no_auth)]

Client = Annotated[AsyncClient, Depends(AuthController.auth_client)]

User = Annotated[UUID4, Depends(current_user)]
