import trio


class Subscriber:

    def __init__(self, predicate):
        self.predicate = predicate
        self.sender = None
        self.receiver = None

    async def __aenter__(self):
        self.sender, self.receiver = trio.open_memory_channel(0)
        await self.sender.__aenter__()
        await self.receiver.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.sender.__aexit__(*args)
        await self.receiver.__aexit__(*args)
