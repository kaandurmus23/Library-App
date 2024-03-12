import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from proje.adapters.orm import metadata, start_mappers
from proje.domain.model import Book, Member
from proje.service_layer import unit_of_work
from proje.domain.event import BookBorrowedEvent, BookReturnedEvent

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        metadata.create_all(cls.engine)
        start_mappers()

    @classmethod
    def tearDownClass(cls):
        clear_mappers()

    def setUp(self):
        self.session = sessionmaker(bind=self.engine)()
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=lambda: self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

class TestHandlers(TestBase):

    def test_create_and_add_book(self):
        with self.uow as uow:
            book = Book("Test Book")
            uow.books.add(book)
            uow.commit()
            book_id = book.book_id

        with self.uow as uow:
            book = uow.books.get(book_id)
            self.assertIsNotNone(book)
            self.assertEqual(book.name, "Test Book")

    def test_create_and_add_member(self):
        with self.uow as uow:
            member = Member("Test Member")
            uow.members.add(member)
            uow.commit()
            member_id = member.member_id

        with self.uow as uow:
            member = uow.members.get(member_id)
            self.assertIsNotNone(member)
            self.assertEqual(member.name, "Test Member")

    def test_borrow_book_for_member(self):
        with self.uow as uow:
            book = Book("Test Book")
            member = Member("Test Member")
            uow.books.add(book)
            uow.members.add(member)
            uow.commit()
            book_id = book.book_id
            member_id = member.member_id

        with self.uow as uow:
            uow.members.get(member_id)
            result = member.borrow_book(book_id)
            self.assertTrue(result)
            uow.commit()

            events = member.domain_events
            self.assertTrue(any(isinstance(event, BookBorrowedEvent) for event in events))

    def test_return_book_for_member(self):
        with self.uow as uow:
            book = Book("Test Book")
            member = Member("Test Member")
            uow.books.add(book)
            uow.members.add(member)
            member.borrow_book(book.book_id)
            uow.commit()
            book_id = book.book_id
            member_id = member.member_id

        with self.uow as uow:
            uow.members.get(member_id)
            result = member.return_book(book_id)
            self.assertTrue(result)
            uow.commit()

            events = member.domain_events
            self.assertTrue(any(isinstance(event, BookReturnedEvent) for event in events))

if __name__ == '__main__':
    unittest.main()
