import trio
from async_vk_bot import Bot


async def echo(bot):
    async for event in bot.sub(lambda e: e['type'] == 'message_new'):
        await bot.api.messages.send(
            peer_id=event['object']['peer_id'],
            message=event['object']['text']
        )


async def main():
    bot = Bot()
    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(echo, bot)


if __name__ == '__main__':
    trio.run(main)
