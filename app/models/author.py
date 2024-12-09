from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base

from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .book import Book


class Author(IntIdPkMixin, Base):

    __tablename__ = "authors"

    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    date_of_birth: Mapped[date] = mapped_column(nullable=False)

    book: Mapped[list["Book"]] = relationship("Book",back_populates="author")
