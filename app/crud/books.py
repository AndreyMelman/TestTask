from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from models import Author
from schemas.book import BookCreate, BookUpdate
from models.book import Book


async def create_book(
    session: AsyncSession,
    book_in: BookCreate,
) -> Book:
    stmt = select(Author).where(Author.id == book_in.author_id)
    result: Result = await session.execute(stmt)
    author = result.scalars().first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Author with id {book_in.author_id} does not exist",
        )

    book = Book(**book_in.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_books(
    session: AsyncSession,
) -> list[Book]:
    stmt = select(Book).order_by(Book.id)
    result: Result = await session.execute(stmt)
    books = result.scalars().all()
    return list(books)


async def get_book(
    session: AsyncSession,
    book_id: int,
) -> Book | None:
    stmt = select(Book).where(Book.id == book_id)
    result: Result = await session.execute(stmt)
    book = result.scalars().first()
    return book


async def update_book(
    session: AsyncSession,
    book_update: BookUpdate,
    book: Book,
) -> Book:
    stmt = select(Author).where(Author.id == book_update.author_id)
    result: Result = await session.execute(stmt)
    author = result.scalars().first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Author with id {book_update.author_id} does not exist",
        )
    for name, value in book_update.model_dump().items():
        setattr(book, name, value)
    await session.commit()
    return book


async def delete_book(
    session: AsyncSession,
    book: Book,
) -> None:
    await session.delete(book)
    await session.commit()
