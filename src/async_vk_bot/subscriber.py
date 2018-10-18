from types import FunctionType
from dataclasses import dataclass, field

import trio


@dataclass(unsafe_hash=True)
class Subscriber:

    predicate: FunctionType
    sender: trio.abc.SendChannel = field(init=False)
    receiver: trio.abc.ReceiveChannel = field(init=False)

    async def __aenter__(self):
        self.sender, self.receiver = trio.open_memory_channel(0)
        await self.sender.__aenter__()
        await self.receiver.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.sender.__aexit__(*args)
        await self.receiver.__aexit__(*args)
