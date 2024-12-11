import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book


@pytest.mark.asyncio(loop_scope="session")
async def test_borrow_create(client, test_data):
    data = {
        "reader_name": "Andrei Lahunovich",
        "date_of_issue": "1988-10-10T10:00:00",
        "date_return": None,
        "book_id": test_data["book_id"],
    }
    response = await client.post(
        "/api/borrows/",
        json=data,
    )

    assert response.status_code == 201
    content = response.json()
    assert content["reader_name"] == "Andrei Lahunovich"
    assert content["date_return"] is None
    assert content["book_id"] == test_data["book_id"]


@pytest.mark.asyncio(loop_scope="session")
async def test_borrow_create_not_count(client, session: AsyncSession):
    book = Book(title="Test Book", count=0)
    session.add(book)
    await session.commit()

    data = {
        "reader_name": "Ekaterina Lahunovich",
        "date_of_issue": "1989-06-25T10:00:00",
        "date_return": None,
        "book_id": book.id,
    }
    response = await client.post(
        "/api/borrows/",
        json=data,
    )

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "No available copies of the book"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_borrows(client):
    response = await client.get("/api/borrows/")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_borrow(client, test_data):
    response = await client.post(
        "/api/borrows/",
        json={
            "reader_name": "Jane Doe",
            "date_of_issue": "2024-12-10T10:00:00",
            "date_return": None,
            "book_id": test_data["book_id"],
        },
    )
    borrow_id = response.json()["id"]

    response = await client.get(
        f"/api/borrows/{borrow_id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == borrow_id


@pytest.mark.asyncio(loop_scope="session")
async def test_update_borrow(client, test_data):
    response = await client.post(
        "/api/borrows/",
        json={
            "reader_name": "Alex",
            "date_of_issue": "2024-12-10T10:00:00",
            "date_return": None,
            "book_id": test_data["book_id"],
        },
    )
    borrow_id = response.json()["id"]

    return_response = await client.put(
        f"/api/borrows/{borrow_id}/return", json={"date_return": "2024-12-11T16:03:25"}
    )
    assert return_response.status_code == 200
    content = return_response.json()
    assert content["date_return"] == "2024-12-11T16:03:25"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_borrow_conflict(client, test_data):
    response = await client.post(
        "/api/borrows/",
        json={
            "reader_name": "Alex",
            "date_of_issue": "2024-12-10T10:00:00",
            "date_return": None,
            "book_id": test_data["book_id"],
        },
    )
    borrow_id = response.json()["id"]

    return_response = await client.put(
        f"/api/borrows/{borrow_id}/return", json={"date_return": "2024-12-11T16:03:25"}
    )

    assert return_response.status_code == 200

    conflicting_response = await client.put(
        f"/api/borrows/{borrow_id}/return", json={"date_return": "2024-12-12T16:03:25"}
    )

    assert conflicting_response.status_code == 409
    assert conflicting_response.json()["detail"] == "CONFLICT"
