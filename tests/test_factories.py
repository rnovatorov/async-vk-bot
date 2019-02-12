from async_vk_bot.factories import make_bot


def test_make_bot():
    api = object()
    bot = make_bot(api)
    assert bot.api == api
