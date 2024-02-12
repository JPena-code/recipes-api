import secrets

from pydantic import Field
from pydantic import HttpUrl, SecretStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Project Settings and sensitive variables"""
    PROJECT_NAME: str = Field(default='API Recipe e-commerce', )
    VERSION: str = Field('0.1.0', )
    DEBUG: bool = True

    ALGORITHM: str = 'HS256'
    EXPIRATION_TIME: PositiveInt = Field(
        default=3600, # Expiration time of an hour
        description='Expiration time for the JWT tokens'
    )
    SECRET: SecretStr = SecretStr(secrets.token_urlsafe(66))

    SERVICE_KEY: SecretStr
    ANON_KEY: SecretStr
    SUPABASE_URL: HttpUrl

    model_config = SettingsConfigDict(
        validate_default=False,
        env_file=('.local.env', '.prod.env'),
        case_sensitive=True,
    )

settings = Settings()
