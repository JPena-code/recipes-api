from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from postgrest.exceptions import APIError

from app.db import Repository
from app.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('Supabase admin client session')
    try:

        await Repository.init_admin()
        yield
    except APIError as error:
        logger.error(
            'Cannot start Supabase admin client "%s - %s"',
            error.code, error.details
        )
    finally:
        await Repository.close_admin()
