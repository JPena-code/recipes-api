from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app import routers
from app.core.events import lifespan
from app.core.settings import settings
from app.utils.exceptions.handlers import validation_error


app = FastAPI(
    lifespan=lifespan,
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    summary='API madded following well practice for an e-commerce of food')

app.exception_handler(RequestValidationError)(validation_error)

app.include_router(
    routers.router,
    prefix='/api'
)
