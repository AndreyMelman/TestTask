from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from api.authors import router as api_router_authors
from api.books import router as api_router_books
from api.borrows import router as api_borrows

from core.db.dp_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()


app = FastAPI()

app.include_router(api_router_authors)
app.include_router(api_router_books)
app.include_router(api_borrows)


@app.get("/")
async def root():
    return {"message": "Hello"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
