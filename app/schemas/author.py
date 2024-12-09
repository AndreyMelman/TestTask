from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    first_name: Annotated[str | None, Field(max_length=32)] = None
    last_name: Annotated[str | None, Field(max_length=32)] = None
    date_of_birth: date | None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorCreate):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
