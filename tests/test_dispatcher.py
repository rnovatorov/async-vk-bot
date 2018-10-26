from unittest.mock import Mock

import trio
import pytest


async def test_one_waiter(dispatcher, test_event, autojump_clock):
    predicate = Mock()

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        event = await dispatcher.wait(predicate)
        assert event == test_event

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        await dispatcher.pub(test_event)

    predicate.assert_called_once_with(test_event)


async def test_multiple_waiters(dispatcher, test_event, autojump_clock):
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


async def test_wait_cancellation(dispatcher, test_event, autojump_clock):
    predicate = lambda _: False
    timeout = 4

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        with trio.move_on_after(timeout):
            await dispatcher.wait(predicate)
        assert not dispatcher._ch_pairs._set

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        await dispatcher.pub(test_event)


async def test_one_subscriber(dispatcher, test_event, autojump_clock):
    predicate = Mock()

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        async with dispatcher.sub(predicate) as events:
            async for event in events:
                assert event == test_event
                return

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        await dispatcher.pub(test_event)

    predicate.assert_called_once_with(test_event)


async def test_multiple_subscribers(dispatcher, test_event, autojump_clock):
    predicate = Mock()
    n_subscribers = 4

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        async with dispatcher.sub(predicate) as events:
            async for event in events:
                assert event == test_event
                return

    async with trio.open_nursery() as nursery:
        for _ in range(n_subscribers):
            await nursery.start(subscriber)
        await dispatcher.pub(test_event)

    predicate.assert_called_with(test_event)
    assert predicate.call_count == n_subscribers


async def test_sub_cancellation(dispatcher, test_event, autojump_clock):
    predicate = lambda _: False
    timeout = 4

    async def subscriber(task_status=trio.TASK_STATUS_IGNORED):
        task_status.started()
        with trio.move_on_after(timeout):
            async with dispatcher.sub(predicate) as events:
                async for _ in events:
                    pytest.fail()
        assert not dispatcher._ch_pairs._set

    async with trio.open_nursery() as nursery:
        await nursery.start(subscriber)
        await dispatcher.pub(test_event)
