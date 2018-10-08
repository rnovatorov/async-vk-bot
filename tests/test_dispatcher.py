import trio
import pytest

from async_vk_bot.dispatcher import Dispatcher


EVENT_TYPE = 'event_type'
EVENT_OBJECT = 42


async def event_gen():
    await trio.sleep(1)
    yield {
        'type': EVENT_TYPE,
        'object': EVENT_OBJECT
    }


async def test_single_sub_true_predicate(nursery, autojump_clock):
    dispatcher = Dispatcher(event_gen=event_gen)

    def predicate(event):
        assert event['type'] == EVENT_TYPE
        assert event['object'] == EVENT_OBJECT
        return True

    nursery.start_soon(dispatcher)
    await dispatcher.sub(predicate)


async def test_single_sub_false_predicate(nursery, autojump_clock):
    dispatcher = Dispatcher(event_gen=event_gen)

    def predicate(event):
        assert event['type'] == EVENT_TYPE
        assert event['object'] == EVENT_OBJECT
        return False

    nursery.start_soon(dispatcher)
    with trio.move_on_after(5):
        await dispatcher.sub(predicate)
        pytest.fail('Unreachable')
