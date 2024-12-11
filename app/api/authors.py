from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import db_helper
from schemas.author import Author, AuthorCreate, AuthorUpdate
from crud import authors


from .dependencies.load_by_id import author_by_id

router = APIRouter(tags=["Authors"], prefix=settings.api.authors)


@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(
    author_in: AuthorCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await authors.create_author(
        session=session,
        author_in=author_in,
    )


@router.get("/", response_model=list[Author])
async def get_authors(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await authors.get_authors(
        session=session,
    )


@router.get("/{author_id}", response_model=Author)
async def get_author(
    author: Author = Depends(author_by_id),
):
    return author


@router.put("/{author_id}", response_model=AuthorUpdate)
async def update_author(
    author_update: AuthorUpdate,
    session: AsyncSession = Depends(db_helper.getter_session),
    author: Author = Depends(author_by_id),
):
    return await authors.update_author(
        session=session,
        author=author,
        author_update=author_update,
    )


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    session: AsyncSession = Depends(db_helper.getter_session),
    author: Author = Depends(author_by_id),
):
    return await authors.delete_author(
        session=session,
        author=author,
    )
