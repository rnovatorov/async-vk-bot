from unittest.mock import Mock

from async_vk_api.api import Api as _Api

from async_vk_bot.factories import make_poller
from async_vk_bot.poller import \
    ERRNO_HISTORY_OUTDATED, ERRNO_KEY_EXPIRED, ERRNO_DATA_LOST


class Session:

    def __init__(self, events):
        self.events = iter(events)

    async def get(self, *args, **kwargs):
        return await self._request(*args, **kwargs)

    async def _request(self, *_, **__):
        response = Mock()
        response.json.return_value = next(self.events)
        return response


class Api(_Api):

    def __init__(self):
        pass

    async def __call__(self, method_name, **params):
        method_name = method_name.replace('.', '_')
        method = getattr(self, method_name)
        return await method(**params)

    async def groups_getById(self):
        return [{'id': 42}]

    async def groups_getLongPollServer(self, group_id):
        return {
            'server': 'test_server',
            'key': 'test_key',
            'ts': 'test_ts'
        }


async def test_sanity():
    api = Api()
    session = Session([
        {'ts': 0, 'updates': [0]},
        {'failed': ERRNO_HISTORY_OUTDATED, 'ts': 0},
        {'ts': 1, 'updates': [1]},
        {'failed': ERRNO_KEY_EXPIRED},
        {'ts': 2, 'updates': [2, 3]},
        {'failed': ERRNO_DATA_LOST},
        {'ts': 3, 'updates': [4]},
    ])

    poller = make_poller(api=api, session=session)

    assert poller.server is None
    assert poller.key is None
    assert poller.ts is None
    assert poller._group_id is None

    async with poller() as events:
        assert await events.__anext__() == 0
        assert poller.server == 'test_server'
        assert poller.key == 'test_key'
        assert poller.ts == 0
        assert poller._group_id == 42

        assert await events.__anext__() == 1
        assert poller.ts == 1

        assert await events.__anext__() == 2
        assert poller.ts == 2

        assert await events.__anext__() == 3
        assert poller.ts == 2

        assert await events.__anext__() == 4
        assert poller.ts == 3
