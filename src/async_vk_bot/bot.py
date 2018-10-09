import trio
from async_vk_api import Api

from .event import EventManager
from .dispatcher import Dispatcher
from .poller import Poller
from .session import Session


class Bot:

    def __init__(self):
        self.session = Session()
        self.api = Api()
        self.poller = Poller(api=self.api)
        self.dispatcher = Dispatcher(event_gen=self.poller)
        self.event = EventManager(dispatcher=self.dispatcher)

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.dispatcher)
