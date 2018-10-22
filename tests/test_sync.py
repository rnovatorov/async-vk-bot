from async_vk_bot.sync import Channel


async def test_sanity():
    async with Channel(capacity=1) as channel:
        assert not channel.sender._closed
        assert not channel.receiver._closed
        await channel.send(42)
        assert 42 == await channel.recv()
    assert channel.sender._closed
    assert channel.receiver._closed
