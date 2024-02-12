from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from postgrest.exceptions import APIError

from app.db import Repository


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print('Starting admin client session')
    try:
        await Repository.init_admin()
        yield
    except APIError as error:
        print(error.hint)
        print(error.code)
    finally:
        await Repository.close_admin()
