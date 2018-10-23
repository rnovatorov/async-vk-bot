from async_vk_api import Api

from .dispatcher import Dispatcher
from .poller import Poller


class Bot(Dispatcher):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.api = Api(*args, **kwargs)
        self.poller = Poller(api=self.api)

    async def __call__(self):
        async with self.poller() as events:
            async for event in events:
                await self.pub(event)
