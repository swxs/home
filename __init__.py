import asyncio

from api.PasswordLock.rpc.base_client import select_password_lock


async def run():
    return await select_password_lock("5d983ca57c1f983c50ea8a18")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run())
    print(result)