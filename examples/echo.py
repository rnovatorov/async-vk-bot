import os

import trio
import async_vk_api
import async_vk_bot


def new_message(event):
    return event['type'] == 'message_new'


async def echo_once(bot):
    """
    Waits for a new message and sends the received text back exactly once.
    """
    event = await bot.wait(new_message)
    await bot.api.messages.send(
        peer_id=event['object']['peer_id'],
        message=event['object']['text']
    )


async def echo(bot):
    """
    Waits for new messages and sends the received text back.
    """
    async with bot.sub(new_message) as events:
        async for event in events:
            await bot.api.messages.send(
                peer_id=event['object']['peer_id'],
                message=event['object']['text']
            )


async def main():
    """
    Starts the bot and event handlers.
    """
    access_token = os.getenv('VK_API_ACCESS_TOKEN')
    api = async_vk_api.make_api(access_token, version='5.89')
    bot = async_vk_bot.make_bot(api)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(echo, bot)
        nursery.start_soon(echo_once, bot)


if __name__ == '__main__':
    trio.run(main)
