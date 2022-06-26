import asyncio


def synchronize_async_helper(to_await):
    async_response = []

    async def run_and_capture_result():
        r = await to_await
        async_response.append(r)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    coroutine = run_and_capture_result()
    loop.run_until_complete(coroutine)
    return async_response[0]
