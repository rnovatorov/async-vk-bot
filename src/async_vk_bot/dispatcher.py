from contextlib import asynccontextmanager

import trio

from .utils import aclosed


class Dispatcher:

    def __init__(self):
        self._lock = trio.Lock()
        self._ch_pairs = set()

    async def pub(self, event):
        async with self._lock:
            for ch_send, _ in self._ch_pairs:
                await ch_send.send(event)

    @aclosed
    async def sub(self, predicate, task_status=trio.TASK_STATUS_IGNORED):
        async with self._open_channel() as (_, ch_recv):
            task_status.started()
            async for event in ch_recv:
                if predicate(event):
                    yield event

    async def wait(self, predicate, **kwargs):
        async with self.sub(predicate, **kwargs) as events:
            async for event in events:
                return event

    @asynccontextmanager
    async def _open_channel(self):
        ch_pair = trio.open_memory_channel(0)
        ch_send, ch_recv = ch_pair

        async with ch_send, ch_recv:
            async with self._lock:
                self._ch_pairs.add(ch_pair)

            try:
                yield ch_pair

            finally:
                with trio.open_cancel_scope(shield=True):
                    async with self._lock:
                        self._ch_pairs.remove(ch_pair)
