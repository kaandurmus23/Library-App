from proje.domain.model import Book, Member
from proje.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from proje.domain.event import BookReturnedEvent, BookBorrowedEvent

def create_and_add_book(name: str) -> int:
    with SqlAlchemyUnitOfWork() as uow:
        book = Book(name=name)
        uow.books.add(book)
        uow.commit()
        return book.book_id

def create_and_add_member(name: str) -> int:
    with SqlAlchemyUnitOfWork() as uow:
        member = Member(name=name)
        uow.members.add(member)
        uow.commit()
        return member.member_id

def borrow_book_for_member(book_id: str, member_id: str) -> bool:
    with SqlAlchemyUnitOfWork() as uow:
        member = uow.members.get(member_id)
        if member and member.borrow_book(book_id):
            uow.commit()
            return True
        return False

def return_book_for_member(book_id: str, member_id: str) -> bool:
    with SqlAlchemyUnitOfWork() as uow:
        member = uow.members.get(member_id)
        if member:
            success = member.return_book(book_id)
            if success:
                uow.commit()
                return True
        return False

# Event Handler Functions
def handle_book_borrowed_event(event: BookBorrowedEvent, uow: SqlAlchemyUnitOfWork):
    with uow:
        book = uow.books.get(event.book_id)
        if book:
            book.borrow()
        uow.commit()

def handle_book_returned_event(event: BookReturnedEvent, uow: SqlAlchemyUnitOfWork):
    with uow:
        book = uow.books.get(event.book_id)
        if book:
            book.return_book()
        uow.commit()


EVENT_HANDLERS = {
    BookBorrowedEvent: [handle_book_borrowed_event],
    BookReturnedEvent: [handle_book_returned_event],
}
