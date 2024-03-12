import unittest
from datetime import datetime, timedelta  # Burada timedelta'ı import edin
from proje.domain.model import Book, Member  # 'your_module' yerine ilgili modül adını kullanın


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book("Test Book")

    def test_book_borrow(self):
        self.assertTrue(self.book.borrow())
        self.assertFalse(self.book.is_available)

    def test_book_return(self):
        self.book.borrow()
        self.assertTrue(self.book.return_book())
        self.assertTrue(self.book.is_available)

class TestMember(unittest.TestCase):

    def setUp(self):
        self.member = Member("Test Member")
        self.book = Book("Test Book")
        self.book_id = self.book.book_id

    def test_borrow_book(self):
        self.assertTrue(self.member.borrow_book(self.book_id))
        self.assertIn(self.book_id, self.member.borrowed_books)

    def test_return_book_no_fees(self):
        self.member.borrow_book(self.book_id)
        self.assertTrue(self.member.return_book(self.book_id))
        self.assertNotIn(self.book_id, self.member.borrowed_books)
        self.assertEqual(self.member.debt, 0)

    def test_return_book_with_fees(self):
        self.member.borrow_book(self.book_id)
        # Simulate a late return (more than 30 days)
        late_return_date = datetime.now() - timedelta(days=31)
        self.member.borrowed_books[self.book_id] = late_return_date.isoformat()
        self.assertTrue(self.member.return_book(self.book_id))
        self.assertGreater(self.member.debt, 0)
if __name__ == '__main__':
    unittest.main()
