# unit_of_work.py
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from proje.config import Config
from proje.adapters.repository import SqlAlchemyBookRepository, SqlAlchemyMemberRepository

class AbstractUnitOfWork(abc.ABC):
    books: SqlAlchemyBookRepository
    members: SqlAlchemyMemberRepository

    def __enter__(self) -> 'AbstractUnitOfWork':
        self.session = self.session_factory()
        self.books = SqlAlchemyBookRepository(self.session)
        self.members = SqlAlchemyMemberRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
    )
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
        self._committed = False

    def __enter__(self):
        self.session = self.session_factory()
        self.books = SqlAlchemyBookRepository(self.session)
        self.members = SqlAlchemyMemberRepository(self.session)
        self._committed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and not self._committed:
            self.rollback()
        self.session.close()

    def _commit(self):
        self.session.commit()
        self._committed = True

    def rollback(self):
        self.session.rollback()
