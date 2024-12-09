from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.author import AuthorCreate, AuthorUpdate
from models.author import Author


async def create_author(
    session: AsyncSession,
    author_in: AuthorCreate,
) -> Author:
    author = Author(**author_in.model_dump())
    session.add(author)
    await session.commit()
    return author


async def get_authors(
    session: AsyncSession,
) -> list[Author]:
    stmt = select(Author).order_by(Author.id)
    result: Result = await session.execute(stmt)
    authors = result.scalars().all()
    return list(authors)


async def get_author(
    session: AsyncSession,
    author_id: int,
) -> Author | None:
    stmt = select(Author).where(Author.id == author_id)
    result: Result = await session.execute(stmt)
    author = result.scalars().first()
    return author


async def update_author(
    session: AsyncSession,
    author_update: AuthorUpdate,
    author: Author,
) -> Author:
    for name, value in author_update.model_dump().items():
        setattr(author, name, value)
    await session.commit()
    return author


async def delete_author(
    session: AsyncSession,
    author: Author,
) -> None:
    await session.delete(author)
    await session.commit()
