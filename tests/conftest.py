import pytest

from async_vk_bot.factories import make_dispatcher


@pytest.fixture()
async def dispatcher():
    return make_dispatcher()
