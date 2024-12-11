from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: Annotated[str, Field(max_length=100)] = None
    description: Annotated[str, Field(max_length=1000)] = None
    count: Annotated[int, Field(ge=0, description="Значение всегда больше 0")] = 0
    author_id: int | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookCreate):
    pass


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

