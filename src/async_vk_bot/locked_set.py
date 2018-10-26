import trio


class LockedSet:

    def __init__(self, seq=()):
        self._set = set(seq)
        self._lock = trio.Lock()

    def __aiter__(self):
        return self.iter()

    async def iter(self):
        async with self._lock:
            for element in self._set:
                yield element

    async def add(self, elem):
        async with self._lock:
            self._set.add(elem)

    async def remove(self, elem):
        async with self._lock:
            self._set.remove(elem)
