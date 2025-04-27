from threading import Lock
from typing import Callable, Set, Dict, Type, List
from events.model import Event

class SingletonMeta(type):
    __instances: Dict = {}
    __lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls] 


class MessageBus(metaclass=SingletonMeta):

    def __init__(self):
        self.registry: Dict[Type, Set[Callable]] = {}

    def register_handler(self, event_type: str):
        def decorator(handler: Callable):
            if self.registry.get(event_type) is None:
                self.registry[event_type] = set()
            self.registry[event_type].add(handler)
            return handler
        return decorator

    def dispatch_event(self, event: Event):
        handlers = self.registry.get(event.event_type, set())
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                continue

    def dispatch_events(self, events: List[Event]):
        for event in events:
            self.dispatch_event(event)

message_bus = MessageBus()