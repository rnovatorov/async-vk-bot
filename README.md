# async-vk-bot

Async VK bot builder built with
[trio](https://github.com/python-trio/trio)
and [async-vk-api](https://github.com/Suenweek/async-vk-api).


## Installation

#### Stable from PyPi
```bash
pip install async-vk-bot
```

#### Latest from Github
```bash
pip install git+https://github.com/Suenweek/async-vk-bot#egg=async-vk-bot
```


## Usage

```python
import trio
from async_vk_bot import Bot


new_message = lambda event: event['type'] == 'message_new'


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
    bot = Bot()
    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(echo, bot)
        nursery.start_soon(echo_once, bot)


if __name__ == '__main__':
    trio.run(main)
```

For the list of event types and objects see
https://vk.com/dev/groups_events.

For more usage see [examples](examples).
