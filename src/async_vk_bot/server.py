import asks
from urllib.parse import urlencode


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
