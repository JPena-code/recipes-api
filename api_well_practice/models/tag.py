from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel
from pydantic import  Field, UUID4, NaiveDatetime

from utils import NameField

class Tag(BaseModel):
    name: NameField

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
