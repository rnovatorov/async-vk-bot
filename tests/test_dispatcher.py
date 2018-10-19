from unittest.mock import Mock

import trio


async def test_one_subscriber(dispatcher, test_event, autojump_clock):
    predicate = Mock()

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        event = await dispatcher.wait(predicate)
        assert event == test_event

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        await dispatcher.pub(test_event)

    predicate.assert_called_once_with(test_event)


async def test_multiple_subscribers(dispatcher, test_event, autojump_clock):
    predicate = Mock()
    n_subscribers = 4

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        event = await dispatcher.wait(predicate)
        assert event == test_event

    async with trio.open_nursery() as nursery:
        for _ in range(n_subscribers):
            await nursery.start(subscriber)
        await dispatcher.pub(test_event)

    predicate.assert_called_with(test_event)
    assert predicate.call_count == n_subscribers


async def test_cancellation(dispatcher, test_event, autojump_clock):
    timeout = 4

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        with trio.move_on_after(timeout):
            await dispatcher.wait(lambda _: False)
        assert not dispatcher._channels

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        await dispatcher.pub(test_event)
