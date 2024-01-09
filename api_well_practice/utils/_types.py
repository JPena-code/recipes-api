from typing import Annotated
from pydantic import StringConstraints, Field


NameField = Annotated[str, StringConstraints(strip_whitespace=True, max_length=50)]
TitleField = Annotated[str, StringConstraints(min_length=20, max_length=80)]
