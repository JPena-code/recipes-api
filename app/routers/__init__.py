from fastapi import APIRouter

from . import v1
from . import auth

router = APIRouter()

router.include_router(auth.router, prefix='', tags=['Auth'])

router_v1 = APIRouter(
    prefix=f'/{v1.API_VERSION}',
    tags=[f'API {v1.__version__}']
)


router_v1.include_router(v1.tag.router, prefix='/tags', tags=['Tags'])
router_v1.include_router(v1.recipe.router, prefix='/recipes', tags=['Recipes'])
router_v1.include_router(v1.category.router, prefix='/categories', tags=['Categories'])
router_v1.include_router(v1.user.router, prefix='/users', tags=['User'])


router.include_router(router_v1)

__all__ = ['router']
