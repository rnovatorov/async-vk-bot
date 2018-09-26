import asks
from urllib.parse import urlencode


class BotsLongPoll:

    ACT = 'a_check'

    def __init__(self, server, key, ts, wait=25):
        self.server = server
        self.key = key
        self.ts = ts
        self.wait = wait

    async def __call__(self):
        return await self.get_events()

    async def get_events(self):
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

    @classmethod
    async def connect(cls, vk_api):
        groups = await vk_api.groups.getById()
        group_id = groups[0]['id']
        blp_cfg = await vk_api.groups.getLongPollServer(group_id=group_id)
        return cls(**blp_cfg)
