import async_vk_api as vk

from . import blp
from .dispatcher import Dispatcher


class Bot(Dispatcher):

    def __init__(self):
        self.vk = vk.Api()
        super().__init__(blp.connect(self.vk))
