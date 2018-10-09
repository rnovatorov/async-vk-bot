import time
from contextlib import contextmanager

import trio

from .utils import aiter, anext


class Dispatcher:

    def __init__(self):
        self._subs = {}

    async def pub(self, event):
        for bucket in list(self._subs.values()):
            await bucket.put(event)

    async def sub(self, predicate):
        with self._bucket() as bucket:
            async for event in bucket:
                if predicate(event):
                    yield event

    async def wait(self, predicate):
        events = aiter(self.sub(predicate))
        event = await anext(events)
        await events.aclose()
        return event

    @contextmanager
    def _bucket(self):
        ts = time.monotonic()
        bucket = trio.Queue(0)
        self._subs[ts] = bucket
        try:
            yield bucket
        finally:
            del self._subs[ts]
