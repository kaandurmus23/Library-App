import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from proje.adapters.orm import metadata, start_mappers
from proje.domain.model import Book, Member
from proje.service_layer.unit_of_work import SqlAlchemyUnitOfWork

class UnitOfWorkTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        metadata.create_all(cls.engine)
        start_mappers()
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        clear_mappers()

    def test_uow_can_add_and_retrieve_a_book(self):
        uow = SqlAlchemyUnitOfWork(session_factory=self.Session)
        book_id = None
        with uow:
            book = Book("Test Book")
            uow.books.add(book)
            book_id = book.book_id
            uow.commit()

        with uow:
            retrieved_book = uow.books.get(book_id)
            book_name = retrieved_book.name  # Oturum içinde özellikleri al

        self.assertEqual("Test Book", book_name)

    def test_uow_rolls_back_uncommitted_changes(self):
        uow = SqlAlchemyUnitOfWork(session_factory=self.Session)
        book_id = None
        with uow:
            book = Book("A Book to Rollback")
            uow.books.add(book)
            book_id = book.book_id
            # Bu noktada commit yapılmıyor

        # Yeni bir oturum açarak nesneyi sorgula
        with self.Session() as new_session:
            retrieved_book = new_session.query(Book).filter_by(book_id=book_id).first()
            self.assertIsNone(retrieved_book)  # Nesne veritabanında olmamalı

    def test_uow_can_add_and_retrieve_a_member(self):
        uow = SqlAlchemyUnitOfWork(session_factory=self.Session)
        member_id = None
        with uow:
            member = Member("Test Member")
            uow.members.add(member)
            member_id = member.member_id
            uow.commit()

        with uow:
            retrieved_member = uow.members.get(member_id)
            member_name = retrieved_member.name

        self.assertEqual("Test Member", member_name)

    def test_member_can_borrow_book(self):
        uow = SqlAlchemyUnitOfWork(session_factory=self.Session)
        book_id = None
        member_id = None
        with uow:
            book = Book("Borrowable Book")
            member = Member("Borrowing Member")
            uow.books.add(book)
            uow.members.add(member)
            member.borrow_book(book.book_id)
            book_id = book.book_id
            member_id = member.member_id
            uow.commit()

        with uow:
            member = uow.members.get(member_id)
            self.assertIsNotNone(member.borrowed_books.get(book_id))


if __name__ == '__main__':
    unittest.main()
