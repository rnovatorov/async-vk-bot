from contextlib import asynccontextmanager

import trio
from async_generator import aclosing

from .sync import LockedSet, Channel


class Dispatcher:

    def __init__(self):
        self._channels = LockedSet()

    async def pub(self, event):
        async for channel in self._channels:
            await channel.send(event)

    def sub(self, predicate):
        async def events():
            async with self._open_channel() as channel:
                async for event in channel:
                    if predicate(event):
                        yield event
        return aclosing(events())

    async def wait(self, predicate):
        async with self.sub(predicate) as events:
            async for event in events:
                return event

    @asynccontextmanager
    async def _open_channel(self):
        async with Channel() as channel:
            await self._channels.add(channel)
            try:
                yield channel
            finally:
                with trio.open_cancel_scope(shield=True):
                    await self._channels.remove(channel)
