from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base
from mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .book import Book

class Borrow(IntIdPkMixin, Base):

    __tablename__ = 'borrows'

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), primary_key=True)
    reader_name: Mapped[str] = mapped_column(String(32))
    date_of_issue: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    date_return: Mapped[datetime]

    book: Mapped[list["Book"]] = relationship(back_populates='borrows')

