from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BorrowBase(BaseModel):
    reader_name: Annotated[str, Field(max_length=32)]
    date_of_issue: datetime
    date_return: datetime | None


class BorrowCreate(BorrowBase):
    pass

class BorrowUpdate(BorrowBase):
    pass

class Borrow(BorrowBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int