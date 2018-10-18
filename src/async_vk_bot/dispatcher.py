from contextlib import asynccontextmanager

import trio

from .utils import aiter, anext
from .subscriber import Subscriber


class Dispatcher:

    def __init__(self):
        self._subs = set()
        self._lock = trio.Lock()

    async def pub(self, event):
        async with self._lock:
            for sub in self._subs:
                if sub.predicate(event):
                    await sub.sender.send(event)

    async def sub(self, predicate):
        async with self._sub_scope(predicate) as sub:
            async for event in sub.receiver:
                yield event

    async def wait(self, predicate):
        events = aiter(self.sub(predicate))
        event = await anext(events)
        await events.aclose()
        return event

    @asynccontextmanager
    async def _sub_scope(self, predicate):
        async with Subscriber(predicate) as sub:
            await self._add_sub(sub)
            try:
                yield sub
            finally:
                with trio.open_cancel_scope(shield=True):
                    await self._remove_sub(sub)

    async def _add_sub(self, sub):
        async with self._lock:
            self._subs.add(sub)

    async def _remove_sub(self, sub):
        async with self._lock:
            self._subs.remove(sub)
