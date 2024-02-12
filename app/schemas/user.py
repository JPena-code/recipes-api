from typing import Any
from pydantic import StrictBool, UUID4

from .base import ModelInDB, Model


class ProfileOut(Model):
    """Response profile schema"""
    name: str
    raw_extra_data: dict[str, Any]

class ProfileInDB(ModelInDB):
    """Response profile schema in Data Base"""
    name: str
    user_id: UUID4
    raw_extra_data: dict[str, Any]
    is_admin: StrictBool
