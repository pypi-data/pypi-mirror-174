import pytest

@pytest.mark.asyncio
async def test_context_session_open_and_close(Parser, useragent):
    async with Parser.create(useragent=useragent) as p:
        assert not p.session.closed
    assert p.session.closed

@pytest.mark.asyncio
async def test_classic_session_open_and_close(Parser, useragent):
    p = Parser(useragent=useragent)
    assert not p.session.closed

    await p.close()
    assert p.session.closed
