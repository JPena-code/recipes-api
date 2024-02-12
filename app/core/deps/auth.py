from typing import Annotated

from fastapi import Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import RefreshToken, Login

oauth_token = HTTPBearer(
    scheme_name='JWTBearer',
    auto_error=False
)

LoginForm = Annotated[Login, Body()]

HTTPCredentials = Annotated[HTTPAuthorizationCredentials, Depends(oauth_token)]

RefreshTokenForm = Annotated[RefreshToken, Depends(RefreshToken.as_from())]
