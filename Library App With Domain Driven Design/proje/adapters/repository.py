import abc
from typing import Set
from sqlalchemy.orm import Session
from proje.domain.model import Book, Member

class AbstractBookRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[Book]

    def add(self, book: Book):
        self._add(book)
        self.seen.add(book)

    def get(self, book_id: str) -> Book:
        book = self._get(book_id)
        if book:
            self.seen.add(book)
        return book

    @abc.abstractmethod
    def _add(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, book_id: str) -> Book:
        raise NotImplementedError

class SqlAlchemyBookRepository(AbstractBookRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, book: Book):
        self.session.add(book)

    def _get(self, book_id: str) -> Book:
        return self.session.query(Book).filter_by(book_id=book_id).first()

class AbstractMemberRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[Member]

    def add(self, member: Member):
        self._add(member)
        self.seen.add(member)

    def get(self, member_id: str) -> Member:
        member = self._get(member_id)
        if member:
            self.seen.add(member)
        return member

    @abc.abstractmethod
    def _add(self, member: Member):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, member_id: str) -> Member:
        raise NotImplementedError

class SqlAlchemyMemberRepository(AbstractMemberRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, member: Member):
        self.session.add(member)

    def _get(self, member_id: str) -> Member:
        return self.session.query(Member).filter_by(member_id=member_id).first()
