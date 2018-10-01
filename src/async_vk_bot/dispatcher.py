from collections import defaultdict
import trio


class Dispatcher:

    def __init__(self, events):
        self._events = events
        self._handlers = defaultdict(list)

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            async for event in self._events:
                for handler in self._handlers[event['type']]:
                    nursery.start_soon(handler, event['object'])

    def on(self, event_type):
        """Decorator version of `self.add_handler`."""
        def decorator(func):
            self.add_handler(event_type, func)
            return func
        return decorator

    def add_handler(self, event_type, event_handler):
        self._handlers[event_type].append(event_handler)
