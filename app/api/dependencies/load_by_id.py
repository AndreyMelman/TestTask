from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from crud import authors, books
from models.author import Author
from models.book import Book


async def author_by_id(
    author_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.getter_session),
) -> Author:
    author = await authors.get_author(session, author_id)
    if author is not None:
        return author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Author {author_id} not found",
    )


async def book_by_id(
    book_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.getter_session),
) -> Book:
    book = await books.get_book(session, book_id)
    if book is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book {book_id} not found",
    )