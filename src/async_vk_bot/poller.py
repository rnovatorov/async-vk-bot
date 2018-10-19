from urllib.parse import urlencode

import asks


class Poller:

    def __init__(self, api):
        self._api = api

    async def __call__(self):
        server = await self._get_server()
        async for events in server:
            for event in events:
                yield event

    async def _get_server(self):
        groups = await self._api.groups.getById()
        group_id = groups[0]['id']
        cfg = await self._api.groups.getLongPollServer(group_id=group_id)
        return Server(**cfg)


class Server:

    ACT = 'a_check'

    def __init__(self, server, key, ts, wait=25):
        self.server = server
        self.key = key
        self.ts = ts
        self.wait = wait

    def __aiter__(self):
        return self

    async def __anext__(self):
        url = self._make_url()
        response = await asks.get(url)
        payload = response.json()
        self.ts = payload['ts']
        return payload['updates']

    def _make_url(self):
        query = urlencode({
            'act': self.ACT,
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait
        })
        return '?'.join([self.server, query])
