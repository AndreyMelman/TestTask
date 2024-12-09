from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: Annotated[str, Field(min_length=100)] = None
    description: Annotated[str, Field(min_length=1000)] = None
    count: Annotated[int, Field()] = 0


class BookCreate(BookBase):
    pass


class BookUpdate(BookCreate):
    pass


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
