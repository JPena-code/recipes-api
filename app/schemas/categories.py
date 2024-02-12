from ..utils import NameField
from .base import Model, ModelInDB, CommonQueryDepend, ConfigModel


class CategoryIn(ConfigModel):
    """Category Schema sended by the user"""
    name: NameField

class CategoryOut(Model):
    """Category schema from the server"""
    name: NameField

class CategoryFilter(CommonQueryDepend):
    """Category schema of available filters fields"""
    name: NameField | None = None

class CategorySave(CategoryIn, Model):
    """Category schema to update an existing resource"""

class CategoryInDB(ModelInDB, CategoryOut):
    """Category Schema response from data base"""
