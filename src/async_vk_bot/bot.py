import async_vk_api as vk

from .poller import Poller
from .dispatcher import Dispatcher


class Bot(Dispatcher):

    def __init__(self):
        self.vk = vk.Api()
        poller = Poller(self.vk)
        super().__init__(events=poller())
