from .server import Server


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
