import pytest

import async_vk_bot


@pytest.fixture()
def test_event():
    return {
        'type': 'test_type',
        'object': 'test_object'
    }


@pytest.fixture()
async def dispatcher():
    return async_vk_bot.make_dispatcher()
