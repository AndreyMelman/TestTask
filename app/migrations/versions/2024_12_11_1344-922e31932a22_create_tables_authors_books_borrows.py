"""create tables authors books borrows

Revision ID: 922e31932a22
Revises: 
Create Date: 2024-12-11 13:44:48.640085

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "922e31932a22"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=False),
        sa.Column("last_name", sa.String(length=32), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
    )

    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), server_default="", nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
            name=op.f("fk_books_author_id_authors"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )

    op.create_table(
        "borrows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=True),
        sa.Column("reader_name", sa.String(length=32), nullable=False),
        sa.Column(
            "date_of_issue",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("date_return", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
            name=op.f("fk_borrows_book_id_books"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_borrows")),
    )


def downgrade() -> None:
    op.drop_table("borrows")
    op.drop_table("books")
    op.drop_table("authors")
