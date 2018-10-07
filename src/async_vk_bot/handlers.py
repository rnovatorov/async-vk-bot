import time
from contextlib import contextmanager

import trio


class BaseHandler:

    def __init__(self):
        self._buckets = {}

    async def __call__(self, obj):
        for bucket in list(self._buckets.values()):
            await bucket.put(obj)

    async def wait(self, predicate):
        with self._subscribe() as bucket:
            while True:
                obj = await bucket.get()
                if predicate(obj):
                    return obj

    @contextmanager
    def _subscribe(self):
        timestamp = time.monotonic()
        bucket = trio.Queue(0)
        self._buckets[timestamp] = bucket

        try:
            yield bucket
        finally:
            del self._buckets[timestamp]
