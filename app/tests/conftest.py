import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from models import Book
from tests.test_config import engine, SessionFactory
from core.db.base import Base


pytest_plugins = "pytest_asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app),
        base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():
    async with SessionFactory() as session:
        yield session

        await session.rollback()


@pytest.fixture(scope="function")
async def test_data(session: AsyncSession):
    # Добавляем тестовую книгу в базу данных
    book = Book(title="Test Book", count=5)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return {"book_id": book.id}
