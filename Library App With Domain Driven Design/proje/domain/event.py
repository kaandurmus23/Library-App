import datetime

class DomainEvent:
    def __init__(self):
        self.occurred_on = datetime.datetime.now()

class BookBorrowedEvent(DomainEvent):
    def __init__(self, member_id, book_id):
        super().__init__()
        self.member_id = member_id
        self.book_id = book_id

class BookReturnedEvent(DomainEvent):
    def __init__(self, member_id, book_id):
        super().__init__()
        self.member_id = member_id
        self.book_id = book_id
