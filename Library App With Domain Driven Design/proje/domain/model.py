from datetime import datetime, timedelta
from proje.domain.event import BookBorrowedEvent, BookReturnedEvent

import uuid
class Book:
    def __init__(self, name):
        self.book_id = str(uuid.uuid4())
        self.name = name
        self.is_available = True

    def borrow(self):
        if self.can_borrow():
            self.is_available = False
            return True
        return False

    def return_book(self):
        if self.can_return():
            self.is_available = True
            return True
        return False

    def can_borrow(self):
        return self.is_available

    def can_return(self):
        return not self.is_available




class Member:
    def __init__(self, name):
        self.member_id = str(uuid.uuid4())
        self.name = name
        self.borrowed_books = {}
        self.debt = 0.0
        self.domain_events = []

    def borrow_book(self, book_id):
        if book_id not in self.borrowed_books:
            self.borrowed_books[book_id] = datetime.now().isoformat()
            self.domain_events.append(BookBorrowedEvent(member_id=self.member_id, book_id=book_id))
            return True
        return False

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            borrow_date_str = self.borrowed_books.pop(book_id)
            borrow_date = datetime.fromisoformat(borrow_date_str)
            overdue_fee = self.calculate_overdue_fee(borrow_date)
            self.debt += overdue_fee
            self.domain_events.append(BookReturnedEvent(member_id=self.member_id, book_id=book_id))
            return True
        return False

    def calculate_overdue_fee(self, borrow_date):
        due_date = borrow_date + timedelta(days=30)
        if datetime.now() > due_date:
            overdue_days = (datetime.now() - due_date).days
            fee_per_day = 10
            return overdue_days * fee_per_day
        return 0

