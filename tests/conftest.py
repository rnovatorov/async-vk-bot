import pytest

from async_vk_bot.dispatcher import Dispatcher


@pytest.fixture()
def test_event():
    return {
        'type': 'test_type',
        'object': 'test_object'
    }


@pytest.fixture()
async def dispatcher():
    return Dispatcher()
