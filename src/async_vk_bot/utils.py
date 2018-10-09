async def anext(aiterator):
    return await aiterator.__anext__()


def aiter(item):
    return item.__aiter__()
