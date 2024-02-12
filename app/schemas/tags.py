from ..utils import NameField
from .base import ConfigModel, Model, ModelInDB, CommonQueryDepend

class TagIn(ConfigModel):
    """Tag schema sended by user"""
    name: NameField

class TagOut(Model):
    """Tag schema response from the server"""
    name: NameField

class TagFilter(CommonQueryDepend):
    """Tag schema of available filters fields"""
    name: NameField | None = None

class TagSave(TagIn, Model):
    """Tag schema to update an existing resource"""

class TagInDB(ModelInDB, TagOut):
    """Tag schema response from the Data Base"""
