from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AuthorBase(BaseModel):
    first_name: Annotated[str | None, Field(max_length=32)] = None
    last_name: Annotated[str | None, Field(max_length=32)] = None
    date_of_birth: Annotated[date | None, Field()] = None

    @field_validator('date_of_birth', mode='before')
    @classmethod
    def validate_date_of_birth(cls, v):
        if v is None:
            return v
        if isinstance(v, date):
            validated_date = v
        elif isinstance(v, str):
            try:
                validated_date = datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("date_of_birth must be in the format 'YYYY-MM-DD'")
        else:
            raise TypeError("date_of_birth must be a string or a date object")

        if validated_date > date.today():
            raise ValueError("date_of_birth cannot be in the future")

        return validated_date


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorCreate):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
