async def anext(ait):
    return await ait.__anext__()


def aiter(obj):
    return obj.__aiter__()
