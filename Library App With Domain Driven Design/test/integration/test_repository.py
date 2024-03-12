import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from proje.adapters.orm import metadata, start_mappers
from proje.domain.model import Book, Member
from proje.adapters.repository import SqlAlchemyBookRepository, SqlAlchemyMemberRepository


class RepositoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        metadata.create_all(cls.engine)
        start_mappers()
        cls.Session = sessionmaker(bind=cls.engine)

    def test_book_repository_add_and_get(self):
        session = self.Session()
        book_repo = SqlAlchemyBookRepository(session)
        book = Book("Test Book")

        # Veri ekleme
        book_repo.add(book)
        session.commit()

        # Veri çekme ve kontrol
        retrieved_book = book_repo.get(book.book_id)
        self.assertEqual(book.name, retrieved_book.name)

        # Veritabanında olup olmadığını kontrol et
        self.assertIsNotNone(retrieved_book)
        self.assertEqual(retrieved_book.name, "Test Book")

        session.close()

    def test_member_repository_add_and_get(self):
        session = self.Session()
        member_repo = SqlAlchemyMemberRepository(session)
        member = Member("Test Member")

        # Veri ekleme
        member_repo.add(member)
        session.commit()

        # Veri çekme ve kontrol
        retrieved_member = member_repo.get(member.member_id)
        self.assertEqual(member.name, retrieved_member.name)

        # Veritabanında olup olmadığını kontrol et
        self.assertIsNotNone(retrieved_member)
        self.assertEqual(retrieved_member.name, "Test Member")

        session.close()


if __name__ == '__main__':
    unittest.main()
