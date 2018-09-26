import asks
from urllib.parse import urlencode


class BotsLongPoll:

    ACT = 'a_check'

    def __init__(self, server, key, ts, wait=25):
        self.server = server
        self.key = key
        self.ts = ts
        self.wait = wait

    def __aiter__(self):
        return self._event_generator()

    async def _event_generator(self):
        while True:
            for event in await self._get_events():
                yield event

    async def _get_events(self):
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


async def connect(vk_api):
    groups = await vk_api.groups.getById()
    group_id = groups[0]['id']
    blp_cfg = await vk_api.groups.getLongPollServer(group_id=group_id)
    return BotsLongPoll(**blp_cfg)
