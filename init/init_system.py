import asyncio

from apps.system.models.user import User
from apps.system.models.user_auth import UserAuth


async def init_system():
    await User.ensure_indexes()
    await UserAuth.ensure_indexes()


async def main():
    await init_system()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
