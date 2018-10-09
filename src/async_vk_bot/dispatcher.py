import time
from contextlib import contextmanager

import trio


class Dispatcher:

    def __init__(self, event_gen):
        self._event_gen = event_gen
        self._subs = {}

    async def __call__(self):
        async for event in self._event_gen():
            await self.pub(event)

    async def pub(self, event):
        for bucket in list(self._subs.values()):
            await bucket.put(event)

    async def sub(self, predicate):
        with self._bucket() as bucket:
            async for event in bucket:
                if predicate(event):
                    yield event

    @contextmanager
    def _bucket(self):
        ts = time.monotonic()
        bucket = trio.Queue(0)
        self._subs[ts] = bucket
        try:
            yield bucket
        finally:
            del self._subs[ts]
