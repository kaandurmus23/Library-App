from sqlalchemy import MetaData, Table, Column, String, Boolean, Float, JSON
from sqlalchemy.orm import registry
from proje.domain.model import Book, Member

metadata = MetaData()
mapper_registry = registry()

books = Table(
    "books",
    metadata,
    Column("book_id", String(255), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("is_available", Boolean, nullable=False, default=True)
)

members = Table(
    "members",
    metadata,
    Column("member_id", String(255), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("borrowed_books", JSON),  # Ödünç alınan kitapların listesi
    Column("debt", Float, nullable=False, default=0.0),
    Column("events", JSON)
)


def start_mappers():
    book_mapper = mapper_registry.map_imperatively(Book, books, primary_key=[books.c.book_id])

    member_mapper = mapper_registry.map_imperatively(Member, members, primary_key=[members.c.member_id], properties={
        'borrowed_books': members.c.borrowed_books,
        'events': members.c.events
    })