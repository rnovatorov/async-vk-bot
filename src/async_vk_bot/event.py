class Event:

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def __getattr__(self, event_type):

        async def wait(predicate=lambda _: True):
            event = await self._dispatcher.sub(lambda event: (
                event['type'] == event_type
                and
                predicate(event['object'])
            ))
            return event['object']

        return wait
