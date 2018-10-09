from .utils import anext, aiter


class Wait:

    def __init__(self, dispatcher, event_type, predicate):
        self._dispatcher = dispatcher
        self._event_type = event_type
        self._predicate = self._wrap_predicate(predicate)

    def __aiter__(self):
        return self._events()

    async def one(self):
        events = aiter(self)
        event = await anext(events)
        await events.aclose()
        return event['object']

    async def _events(self):
        async for event in self._dispatcher.sub(self._predicate):
            yield event['object']

    def _wrap_predicate(self, predicate):
        def wrapper(event):
            return (
                event['type'] == self._event_type
                and
                predicate(event['object'])
            )
        return wrapper


class Event:

    def __init__(self, dispatcher, type):
        self._dispatcher = dispatcher
        self._type = type

    def __call__(self, predicate=lambda _: True):
        return Wait(
            dispatcher=self._dispatcher,
            event_type=self._type,
            predicate=predicate
        )


class EventManager:

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def __getattr__(self, event_type):
        return Event(
            dispatcher=self._dispatcher,
            type=event_type
        )
