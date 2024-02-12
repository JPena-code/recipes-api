from typing import Annotated, TypeAlias

from fastapi import Path, File
from fastapi.datastructures import UploadFile

from pydantic import UUID4
from pydantic import StringConstraints

from postgrest.base_request_builder import APIResponse, SingleAPIResponse

MultipleResponse: TypeAlias = APIResponse
SingleResponse: TypeAlias = SingleAPIResponse

NameField = Annotated[str, StringConstraints(strip_whitespace=True, max_length=80)]
TitleField = Annotated[str, StringConstraints(min_length=10, max_length=200)]

PathID = Annotated[UUID4, Path(..., description='ID of the resource to get', )]
# TODO: Add None in Annotated
ImageFile = Annotated[UploadFile, File(description='Image file for the recipes')]
