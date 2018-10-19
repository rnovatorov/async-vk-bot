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


class Channel:

    def __init__(self, capacity=0):
        self.capacity = capacity
        self.sender = None
        self.receiver = None

    async def __aenter__(self):
        self.sender, self.receiver = trio.open_memory_channel(self.capacity)
        await self.sender.__aenter__()
        await self.receiver.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.sender.__aexit__(*args)
        await self.receiver.__aexit__(*args)

    def __aiter__(self):
        return self.receiver.__aiter__()

    async def send(self, value):
        await self.sender.send(value)

    async def recv(self):
        return await self.receiver.receive()
