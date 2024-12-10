from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BorrowBase(BaseModel):
    reader_name: Annotated[str, Field(max_length=32)]
    date_of_issue: datetime = Field(default=datetime.now())
    date_return: datetime | None
    book_id: int


class BorrowCreate(BorrowBase):
    date_return: None


class BorrowUpdate(BaseModel):
    date_return: datetime = Field(default=datetime.now())


class Borrow(BorrowBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
