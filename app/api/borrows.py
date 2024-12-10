from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import db_helper
from schemas.borrow import Borrow, BorrowCreate, BorrowUpdate

from crud import borrows
from api.dependencies.load_by_id import borrow_by_id

router = APIRouter(tags=["Borrows"], prefix=settings.api.borrows)


@router.post("/", response_model=Borrow, status_code=status.HTTP_201_CREATED)
async def borrow_create(
    borrow_in: BorrowCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
) -> Borrow:
    return await borrows.create_borrow(
        session=session,
        borrow_in=borrow_in,
    )


@router.get("/", response_model=list[Borrow])
async def get_borrows(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await borrows.get_borrows(
        session=session,
    )


@router.get("/{borrow_id}", response_model=Borrow)
async def get_borrow(
    borrow: Borrow = Depends(borrow_by_id),
):
    return borrow


@router.put("/{borrow_id}/return", response_model=Borrow)
async def update_borrow(
    borrow_update: BorrowUpdate,
    session: AsyncSession = Depends(db_helper.getter_session),
    borrow: Borrow = Depends(borrow_by_id),
):
    return await borrows.update_borrow(
        session=session,
        borrow=borrow,
        borrow_update=borrow_update,
        partial=True,
    )
