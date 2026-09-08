# -*- coding: utf-8 -*-
# @File    : repositories/user_identity_repository.py
# @AUTH    : code_creater

"""身份聚合 Repository：跨 User 与 UserAuth 的身份查询与 find-or-create。

与表级 Repository 不同，本聚合 Repository 跨多表取数/写入并返回 ORM 对象，
仅做 flush（由 service 通过 transaction 统一 commit），事务边界永远在 service。
表级 repo 以 Repo(session) 构造（model 为类属性），可选注入便于单测。
"""

from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from home.web.schemas.types import objectId
# 本模块方法
from .. import consts
from ..models.user import User
from ..models.user_auth import UserAuth
from ..schemas.user import UserSchema
from ..schemas.user_auth import UserAuthSchema
from .user_auth_repository import UserAuthRepository
from .user_repository import UserRepository


class UserIdentityRepository:
    """User + UserAuth 身份解析。仅 flush，不 commit。"""

    def __init__(
        self,
        session: AsyncSession,
        user_repo: Optional[UserRepository] = None,
        user_auth_repo: Optional[UserAuthRepository] = None,
    ):
        self.session = session
        self.user_repo = user_repo or UserRepository(session)
        self.user_auth_repo = user_auth_repo or UserAuthRepository(session)

    async def find_user_auth(self, user_auth_schema: UserAuthSchema) -> Optional[UserAuth]:
        """按条件查询单条用户认证记录。"""
        return await self.user_auth_repo.find_one_or_none(user_auth_schema)

    async def find_user(self, user_id: objectId) -> Optional[User]:
        """按主键查询用户。"""
        return await self.user_repo.find_one(user_id)

    async def create_user_with_auth(
        self,
        user_schema: UserSchema,
        user_auth_schema: UserAuthSchema,
    ) -> Tuple[User, UserAuth]:
        """创建用户并绑定认证信息，返回 (User, UserAuth)。仅 flush。"""
        user = await self.user_repo.create_one(user_schema)
        user_auth_schema.user_id = user.id
        user_auth = await self.user_auth_repo.create_one(user_auth_schema)
        return user, user_auth

    async def find_user_by_username(self, username: str) -> Optional[User]:
        return await self.user_repo.find_one_or_none(UserSchema(username=username))

    async def find_auths_by_user_id(self, user_id: objectId) -> List[UserAuth]:
        return await self.user_auth_repo.find_by_user_ids([user_id])

    async def create_user_with_password_and_email(
        self,
        username: str,
        email: str,
        password_hash: str,
    ) -> Tuple[User, UserAuth, UserAuth]:
        user = await self.user_repo.create_one(UserSchema(username=username))
        password_auth = await self.user_auth_repo.create_one(
            UserAuthSchema(
                user_id=user.id,
                ttype=consts.UserAuth_Ttype.PASSWORD,
                identifier=username,
                credential=password_hash,
                ifverified=consts.UserAuth_Ifverified.UNVERIFIED,
            )
        )
        email_auth = await self.user_auth_repo.create_one(
            UserAuthSchema(
                user_id=user.id,
                ttype=consts.UserAuth_Ttype.EMAIL,
                identifier=email,
                credential=None,
                ifverified=consts.UserAuth_Ifverified.UNVERIFIED,
            )
        )
        return user, password_auth, email_auth

    async def verify_user_auths(self, user_id: objectId) -> None:
        auths = await self.find_auths_by_user_id(user_id)
        for auth in auths:
            if auth.ttype in (consts.UserAuth_Ttype.PASSWORD, consts.UserAuth_Ttype.EMAIL):
                await self.user_auth_repo.update_one(
                    str(auth.id),
                    UserAuthSchema(ifverified=consts.UserAuth_Ifverified.VERIFIED),
                )

    async def update_password_credential(self, user_id: objectId, password_hash: str) -> None:
        password_auth = await self.user_auth_repo.find_one_or_none(
            UserAuthSchema(
                user_id=user_id,
                ttype=consts.UserAuth_Ttype.PASSWORD,
            )
        )
        if password_auth is None:
            return
        await self.user_auth_repo.update_one(
            str(password_auth.id),
            UserAuthSchema(credential=password_hash),
        )

    async def resolve_or_create_github_user(
        self,
        github_id: str,
        github_username: str,
        github_email: str,
        access_token: str,
    ) -> User:
        """解析 GitHub 身份：优先 GitHub 认证，其次邮箱认证，否则新建用户并绑定 GitHub 认证。

        返回对应 User（ORM）。仅 flush，commit 由 service 的 transaction 负责。
        """
        github_auth = await self.user_auth_repo.find_one_or_none(
            UserAuthSchema(
                ttype=consts.UserAuth_Ttype.GITHUB,
                identifier=github_id,
                ifverified=consts.UserAuth_Ifverified.VERIFIED,
            )
        )
        if github_auth:
            return await self.user_repo.find_one(str(github_auth.user_id))

        email_auth = await self.user_auth_repo.find_one_or_none(
            UserAuthSchema(
                ttype=consts.UserAuth_Ttype.EMAIL,
                identifier=github_email,
                ifverified=consts.UserAuth_Ifverified.VERIFIED,
            )
        )
        if email_auth:
            user = await self.user_repo.find_one(str(email_auth.user_id))
        else:
            user = await self.user_repo.create_one(UserSchema(username=github_username))

        await self.user_auth_repo.create_one(
            UserAuthSchema(
                user_id=user.id,
                ttype=consts.UserAuth_Ttype.GITHUB,
                identifier=github_id,
                credential=access_token,
                ifverified=consts.UserAuth_Ifverified.VERIFIED,
            )
        )
        return user
