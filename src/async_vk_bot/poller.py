from urllib.parse import urlencode

import asks

from .utils import aclosed


DEFAULT_WAIT = 25
ACT = 'a_check'

ERRNO_HISTORY_OUTDATED = 1
ERRNO_KEY_EXPIRED = 2
ERRNO_DATA_LOST = 3


class Poller:

    def __init__(self, api, wait=DEFAULT_WAIT):
        self.api = api
        self.wait = wait

        self._group_id = None

        self.server = None
        self.key = None
        self.ts = None

    def __call__(self):
        return self.poll()

    @aclosed
    async def poll(self):
        await self._init()
        while True:
            events = await self._wait_events()
            for event in events:
                yield event

    async def _init(self):
        config = await self._get_config()
        self.server = config['server']
        self.key = config['key']
        self.ts = config['ts']

    async def _wait_events(self):
        url = self._make_url()
        response = await asks.get(url)
        payload = response.json()

        errno = payload.get('failed')

        if errno is None:
            self.ts = payload['ts']
            return payload['updates']

        if errno == ERRNO_HISTORY_OUTDATED:
            self.ts = payload['ts']

        elif errno == ERRNO_KEY_EXPIRED:
            config = await self._get_config()
            self.key = config['key']

        elif errno == ERRNO_DATA_LOST:
            config = await self._get_config()
            self.key = config['key']
            self.ts = config['ts']

        else:
            raise RuntimeError(f'Unexpected errno: {errno}')

        return []

    async def _get_config(self):
        group_id = await self._get_group_id()
        config = await self.api.groups.getLongPollServer(
            group_id=group_id
        )
        return config

    async def _get_group_id(self):
        if self._group_id is None:
            groups = await self.api.groups.getById()
            self._group_id = groups[0]['id']
        return self._group_id

    def _make_url(self):
        query = urlencode({
            'act': ACT,
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait
        })
        return '?'.join([self.server, query])
