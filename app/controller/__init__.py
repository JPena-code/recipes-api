from .tag import _TagsController
from .recipe import _RecipesController
from .category import _CategoriesController

CategoriesController = _CategoriesController()
RecipesController = _RecipesController()
TagsController = _TagsController()

__all__ = [
    'TagsController',
    'RecipesController',
    'CategoriesController',
]
