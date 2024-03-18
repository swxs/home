import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

import core
from apps.memo.models.todo import Todo
from apps.password_lock.models.password_lock import PasswordLock
from apps.system.models.user_auth_model import UserAuth
from apps.system.models.user_model import User
from apps.wechat.models.wechat_msg import WechatMsg

core.mongodb_database.client = AsyncIOMotorClient(core.config.MONGODB_URI)

loop = asyncio.get_event_loop()
loop.run_until_complete(User.ensure_indexes())
loop.run_until_complete(UserAuth.ensure_indexes())
loop.run_until_complete(Todo.ensure_indexes())
loop.run_until_complete(PasswordLock.ensure_indexes())
loop.run_until_complete(WechatMsg.ensure_indexes())

core.mongodb_database.client.close()
