from uuid import uuid4
from typing import List
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field, NaiveDatetime, UUID4, AnyHttpUrl

from . import Category, Tag
from utils import TitleField

class Recipe(BaseModel):

    category: Category
    title: TitleField
    description: str
    instructions: str
    image: AnyHttpUrl = Field(
        default=None,
        description='URL for an image that represents the recipe')
    # TODO: Think how to mage the pivot table
    tags: List[Tag] = Field(
        default=None,
        description='Tags that describe the Recipe'
    )
    # TODO: fix later to use a real user
    user_id: UUID4
    # Metadata info for the class
    id: UUID4 = Field(
        default_factory=uuid4,
        frozen=True,
        description='Name of the tag associated to one category')
    created_at: NaiveDatetime = Field(
        default_factory=datetime.now,
        description='Timestamp of the tag',
        frozen=True)
    updated_at: NaiveDatetime = Field(
        default_factory=datetime.now,
        description='Timestamp of the update madded to a tag',
        frozen=True)
