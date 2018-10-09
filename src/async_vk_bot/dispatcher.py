from contextlib import contextmanager

import trio

from .utils import aiter, anext


class Dispatcher:

    def __init__(self):
        self._buckets = set()

    async def pub(self, event):
        for bucket in list(self._buckets):
            await bucket.put(event)

    async def sub(self, predicate):
        with self._open_bucket() as bucket:
            async for event in bucket:
                if predicate(event):
                    yield event

    async def wait(self, predicate):
        events = aiter(self.sub(predicate))
        event = await anext(events)
        await events.aclose()
        return event

    @contextmanager
    def _open_bucket(self):
        bucket = trio.Queue(0)
        self._buckets.add(bucket)
        try:
            yield bucket
        finally:
            self._buckets.remove(bucket)
