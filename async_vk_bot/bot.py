import os
import asks
import trio
import async_vk_api as vk
from .blp import BotsLongPoll


Q_SIZE = 8


async def receiver(api, q):
    blp = await BotsLongPoll.connect(api)
    while True:
        events = await blp()
        for event in events:
            await q.put(event)


async def sender(api, q):
    while True:
        event = await q.get()
        if event['type'] == 'message_new' and event['object']['text']:
            await api.messages.send(
                peer_id=event['object']['peer_id'],
                message=event['object']['text']
            )


async def dispatcher():
    access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_api = vk.Api(access_token)

    q = trio.Queue(Q_SIZE)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(receiver, vk_api, q)
        nursery.start_soon(sender, vk_api, q)


def main():
    asks.init('trio')
    trio.run(dispatcher)
