import trio

from async_vk_bot.dispatcher import Dispatcher
from async_vk_bot.handlers import BaseHandler


EVENT_TYPE = 'event_type'
EVENT_OBJECT = 42


async def events():
    await trio.sleep(1)
    yield {
        'type': EVENT_TYPE,
        'object': EVENT_OBJECT
    }
    await trio.sleep(1)


async def test_base_handler_true_predicate(autojump_clock, nursery):
    dispatcher = Dispatcher(events=events())
    handler = BaseHandler()
    dispatcher.add_handler(EVENT_TYPE, handler)
    nursery.start_soon(dispatcher)

    await handler.wait(lambda _: True)

    assert not handler._buckets


async def test_base_handler_false_predicate(autojump_clock, nursery):
    dispatcher = Dispatcher(events=events())
    handler = BaseHandler()
    dispatcher.add_handler(EVENT_TYPE, handler)
    nursery.start_soon(dispatcher)

    with trio.move_on_after(5):
        await handler.wait(lambda _: False)

    assert not handler._buckets


async def test_base_handler_multiple_waiters(autojump_clock, nursery):
    n_waiters = 4

    dispatcher = Dispatcher(events=events())
    handler = BaseHandler()
    dispatcher.add_handler(EVENT_TYPE, handler)
    nursery.start_soon(dispatcher)

    finished = trio.Event()

    for _ in range(n_waiters):
        nursery.start_soon(handler.wait, lambda _: finished.is_set())

    await trio.sleep(1)
    assert len(handler._buckets) == n_waiters

    finished.set()

    await trio.sleep(1)
    assert not handler._buckets
