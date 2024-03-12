from typing import Callable, Dict, List, Type
from proje.domain import event
from proje.service_layer import unit_of_work

class MessageBus:
    def __init__(self, uow: unit_of_work.AbstractUnitOfWork, event_handlers: Dict[Type[event.DomainEvent], List[Callable]]):
        self.uow = uow
        self.event_handlers = event_handlers

    def handle_event(self, event: event.DomainEvent):
        for handler in self.event_handlers[type(event)]:
            handler(event, self.uow)
