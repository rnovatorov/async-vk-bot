import trio

from async_vk_bot.dispatcher import Dispatcher


TEST_EVENT_TYPE = 'test_event_type'
TEST_EVENT_OBJECT = 42


async def single_event():
    await trio.sleep(1)
    yield {
        'type': TEST_EVENT_TYPE,
        'object': TEST_EVENT_OBJECT
    }
    await trio.sleep(1)


async def multiple_events(n=3):
    for _ in range(n):
        yield await single_event().__anext__()


async def test_single_event_to_single_handler(autojump_clock):
    dispatcher = Dispatcher(events=single_event())

    @dispatcher.on(TEST_EVENT_TYPE)
    async def handler(obj):
        assert obj == TEST_EVENT_OBJECT

    await dispatcher()


async def test_single_event_to_multiple_handlers(autojump_clock):
    n_handlers = 4
    handler_calls = 0

    dispatcher = Dispatcher(events=single_event())

    async def handler(obj):
        nonlocal handler_calls
        handler_calls += 1
        assert obj == TEST_EVENT_OBJECT

    for _ in range(n_handlers):
        dispatcher.add_handler(TEST_EVENT_TYPE, handler)

    await dispatcher()

    assert handler_calls == n_handlers


async def test_multiple_events_to_multiple_handlers(autojump_clock):
    n_events = 4
    n_handlers = 4
    handler_calls = 0

    dispatcher = Dispatcher(events=multiple_events(n=n_events))

    async def handler(obj):
        nonlocal handler_calls
        handler_calls += 1
        assert obj == TEST_EVENT_OBJECT

    for _ in range(n_handlers):
        dispatcher.add_handler(TEST_EVENT_TYPE, handler)

    await dispatcher()

    assert handler_calls == n_handlers * n_events
