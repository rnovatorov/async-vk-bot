from collections import defaultdict
import trio


class Dispatcher:

    def __init__(self, event_generator, q_size=1, n_workers=1):
        self._event_generator = event_generator
        self._event_queue = trio.Queue(q_size)
        self._n_workers = n_workers
        self._event_handlers = defaultdict(list)

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self._producer)
            for _ in range(self._n_workers):
                nursery.start_soon(self._consumer)

    def on(self, event_type):
        """
        Decorator version of `self.add_event_handler`.
        """
        def decorator(func):
            self.add_event_handler(event_type, func)
            return func
        return decorator

    def add_event_handler(self, event_type, event_handler):
        self._event_handlers[event_type].append(event_handler)

    async def _producer(self):
        async for event in await self._event_generator:
            await self._event_queue.put(event)

    async def _consumer(self):
        async for event in self._event_queue:
            await self._dispatch(event)

    async def _dispatch(self, event):
        for event_handler in self._event_handlers[event['type']]:
            await event_handler(event['object'])
