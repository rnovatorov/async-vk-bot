import trio

from async_vk_bot.utils import aclosed
from async_vk_bot.factories import make_bot


async def test_bot(dispatcher):
    api = object()

    @aclosed
    async def poller():
        yield 42

    bot = make_bot(api=api, poller=poller, dispatcher=dispatcher)

    assert bot.__call__ == bot.run
    assert bot.api == api
    assert bot.pub == dispatcher.pub
    assert bot.sub == dispatcher.sub
    assert bot.wait == dispatcher.wait

    async def subscriber(**kwargs):
        event = await bot.wait(lambda _: True, **kwargs)
        assert event == 42
        nursery.cancel_scope.cancel()

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        nursery.start_soon(bot)
