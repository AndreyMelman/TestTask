from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .book import Book

class Borrow(IntIdPkMixin, Base):

    __tablename__ = 'borrows'

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    reader_name: Mapped[str] = mapped_column(String(32))
    date_of_issue: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    date_return: Mapped[datetime]

    book: Mapped["Book"] = relationship("Book", back_populates='borrows')

