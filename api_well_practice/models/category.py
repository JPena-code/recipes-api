from datetime import datetime

from uuid import uuid4
from pydantic import BaseModel
from pydantic import  Field, StringConstraints, UUID4, NaiveDatetime

from utils import NameField

class Category(BaseModel):
    name: NameField

    # Metadata info for the class
    id: UUID4 = Field(
        default_factory=uuid4,
        frozen=True,
        description='Name of the category added')
    created_at: NaiveDatetime = Field(
        default_factory=datetime.now,
        description='Timestamp of the category',
        frozen=True)
    updated_at: NaiveDatetime = Field(
        default_factory=datetime.now,
        description='Timestamp of the update madded to a category',
        frozen=True)
