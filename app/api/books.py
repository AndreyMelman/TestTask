from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.load_by_id import book_by_id
from core.config import settings
from core.db import db_helper
from schemas.book import BookCreate, Book, BookUpdate

from crud import books

router = APIRouter(tags=["Books"], prefix=settings.api.books)


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_author(
    book_in: BookCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await books.create_book(
        session=session,
        book_in=book_in,
    )


@router.get("/", response_model=list[Book])
async def get_books(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await books.get_books(
        session=session,
    )


@router.get("/{book_id}", response_model=Book)
async def get_book(
    book: Book = Depends(book_by_id),
):
    return book


@router.put("/{book_id}", response_model=BookUpdate)
async def update_book(
    author_update: BookUpdate,
    book: Book = Depends(book_by_id),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await books.update_book(
        session=session,
        book_update=author_update,
        book=book,
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    session: AsyncSession = Depends(db_helper.getter_session),
    book: Book = Depends(book_by_id),
):
    return await books.delete_book(
        session=session,
        book=book,
    )
