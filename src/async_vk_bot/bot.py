from async_vk_api import Api

from .dispatcher import Dispatcher
from .poller import Poller


class Bot(Dispatcher):

    def __init__(self):
        super().__init__()
        self.api = Api()
        self.poller = Poller(api=self.api)

    async def __call__(self):
        async for event in self.poller():
            await self.pub(event)
