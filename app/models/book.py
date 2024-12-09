from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base
from mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .borrow import Borrow
    from .author import Author


class Book(IntIdPkMixin, Base):

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    count: Mapped[int] = mapped_column(Integer, default=0)

    author: Mapped[list["Author"]] = relationship(back_populates="books")
    borrow: Mapped[list["Borrow"]] = relationship(back_populates="books")
