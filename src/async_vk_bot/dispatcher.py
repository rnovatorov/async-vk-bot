from contextlib import asynccontextmanager

import trio

from .channel import Channel


class Dispatcher:

    def __init__(self):
        self._channels = set()
        self._lock = trio.Lock()

    async def pub(self, event):
        async with self._lock:
            for channel in self._channels:
                await channel.send(event)

    async def sub(self, predicate):
        async with self._open_channel() as channel:
            async for event in channel:
                if predicate(event):
                    yield event

    async def wait(self, predicate):
        events = self.sub(predicate).__aiter__()
        event = await events.__anext__()
        await events.aclose()
        return event

    @asynccontextmanager
    async def _open_channel(self):
        async with Channel() as channel:
            async with self._lock:
                self._channels.add(channel)
            try:
                yield channel
            finally:
                with trio.open_cancel_scope(shield=True):
                    async with self._lock:
                        self._channels.remove(channel)
