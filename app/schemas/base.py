from pydantic.alias_generators import to_camel
from pydantic import BaseModel, ConfigDict, Field
from pydantic import UUID4, AwareDatetime, NonNegativeInt, PositiveInt


# TODO: Search how to use the alias in the correct way
class ConfigModel(BaseModel):
    """Config model to not allow extra fields"""
    model_config = ConfigDict(
        extra='ignore',
        loc_by_alias=False,
        # alias_generator=to_camel,
        validate_assignment=True,
    )

class Model(ConfigModel):
    """Base model for the system only have an id"""
    id: UUID4 | None = None

class ModelInDB(Model):
    """Base attributes for a model in DB"""
    # Metadata info for the class
    id: UUID4
    created_at: AwareDatetime
    updated_at: AwareDatetime

class CommonQueryDepend(ConfigModel):
    page: NonNegativeInt | None = Field(default=1, description='Number of the current page requested')
    skip: NonNegativeInt | None = Field(default=0, description='Number items to skip')
    limit: PositiveInt | None = Field(default=100, description='Content length of the page')
