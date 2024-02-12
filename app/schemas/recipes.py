import json

from pydantic import UUID4, AnyHttpUrl
from pydantic.functional_validators import model_validator

from ..utils import TitleField
from .tags import TagInDB, TagOut
from .categories import CategoryInDB, CategoryOut
from .base import Model, ModelInDB, CommonQueryDepend, ConfigModel

class RecipeIn(ConfigModel):
    """Recipe schema sended by the user"""
    title: TitleField
    description: str
    ingredients: str
    instructions: str
    tags: list[UUID4] | None = None
    category_id: UUID4 | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class RecipeOut(Model):
    """Recipe schema from the server"""
    title: TitleField
    description: str
    ingredients: str
    instructions: str
    image: AnyHttpUrl | None = None
    tags: list[TagOut] | None = None
    category: CategoryOut | None = None

class RecipeSave(Model, RecipeIn):
    """Recipe Schema to update an existing resource"""
    user_id: UUID4
    image: AnyHttpUrl | None = None

class RecipeFilter(CommonQueryDepend):
    """Recipe schema of available filters fields"""
    title: TitleField | None = None
    tag: UUID4 | None = None
    category: UUID4 | None = None

class RecipeInDB(RecipeOut, ModelInDB):
    """Recipe schema response from the Data Base"""
    tags: list[TagInDB] = []
    category: CategoryInDB
    user_id: UUID4
