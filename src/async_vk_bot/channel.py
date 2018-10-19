import trio


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
