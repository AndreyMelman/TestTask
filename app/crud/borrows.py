from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Borrow, Book
from schemas.borrow import BorrowCreate, BorrowUpdate


async def create_borrow(
    session: AsyncSession,
    borrow_in: BorrowCreate,
) -> Borrow:
    stmt = select(Book).where(Book.id == borrow_in.book_id)
    result: Result = await session.execute(stmt)
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.count <= 0:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No available copies of the book"
        )

    borrow = Borrow(**borrow_in.model_dump())
    session.add(borrow)

    book.count -= 1
    await session.commit()
    return borrow


async def get_borrows(
    session: AsyncSession,
) -> list[Borrow]:
    stmt = select(Borrow).order_by(Borrow.id)
    result: Result = await session.execute(stmt)
    borrows = result.scalars().all()
    return list(borrows)


async def get_borrow(
    session: AsyncSession,
    borrow_id: int,
) -> Borrow | None:
    stmt = select(Borrow).where(Borrow.id == borrow_id)
    result: Result = await session.execute(stmt)
    borrow = result.scalars().first()
    return borrow


async def update_borrow(
    session: AsyncSession,
    borrow_update: BorrowUpdate,
    borrow: Borrow,
    partial: bool = False,
) -> Borrow:
    if borrow.date_return is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="CONFLICT")

    stmt = select(Book).where(Book.id == borrow.book_id)
    result: Result = await session.execute(stmt)
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")

    for name, value in borrow_update.model_dump(exclude_unset=partial).items():
        setattr(borrow, name, value)

    book.count += 1

    await session.commit()
    return borrow
