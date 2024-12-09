from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from crud import authors
from models.author import Author


async def author_by_id(
    author_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.getter_session),
) -> Author:
    author = await authors.get_author(session, author_id)
    if author is not None:
        return author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {author_id} not found",
    )
