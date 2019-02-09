[![Build Status](https://travis-ci.com/Suenweek/async-vk-bot.svg?branch=master)](https://travis-ci.com/Suenweek/async-vk-bot)
[![codecov](https://codecov.io/gh/Suenweek/async-vk-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/Suenweek/async-vk-bot)

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
    api = async_vk_api.make_api(
        access_token=os.getenv('VK_API_ACCESS_TOKEN'),
        version='5.89'
    )
    bot = async_vk_bot.make_bot(api)

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


## Bots built with async-vk-bot

 - [vk-code-names](https://github.com/Suenweek/vk-code-names)
