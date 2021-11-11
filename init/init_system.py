import asyncio
from apps.System.utils.User import User


async def init_system():
    pass


async def main():
    await init_system()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
