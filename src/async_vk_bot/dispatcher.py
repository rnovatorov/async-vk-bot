from contextlib import asynccontextmanager

import trio

from .utils import aclosed
from .locked_set import LockedSet


class Dispatcher:

    def __init__(self):
        self._ch_pairs = LockedSet()

    async def pub(self, event):
        async for ch_send, _ in self._ch_pairs:
            await ch_send.send(event)

    @aclosed
    async def sub(self, predicate):
        async with self._open_channel() as (_, ch_recv):
            async for event in ch_recv:
                if predicate(event):
                    yield event

    async def wait(self, predicate):
        async with self.sub(predicate) as events:
            async for event in events:
                return event

    @asynccontextmanager
    async def _open_channel(self):
        ch_pair = trio.open_memory_channel(0)
        ch_send, ch_recv = ch_pair
        async with ch_send, ch_recv:
            await self._ch_pairs.add(ch_pair)
            try:
                yield ch_pair
            finally:
                with trio.open_cancel_scope(shield=True):
                    await self._ch_pairs.remove(ch_pair)
