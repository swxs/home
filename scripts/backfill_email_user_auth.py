# -*- coding: utf-8 -*-
"""为历史用户补建 EMAIL 类型 user_auth，并将 PASSWORD/EMAIL 标为已验证（便于继续登录）。

用法（在能连数据库的环境）：
  uv run python scripts/backfill_email_user_auth.py --username swxs --email 466565029@qq.com
  uv run python scripts/backfill_email_user_auth.py --username swxs --email 466565029@qq.com --dry-run
  uv run python scripts/backfill_email_user_auth.py --list-missing
"""

import argparse
import asyncio

from sqlalchemy import select

from home.apps.system import consts
from home.apps.system.models.user import User
from home.apps.system.models.user_auth import UserAuth
from home.apps.system.repositories.user_auth_repository import UserAuthRepository
from home.apps.system.schemas.user_auth import UserAuthSchema
from home.mysqlengine import open_session, transaction


async def list_missing(session) -> None:
    users = (await session.execute(select(User))).scalars().all()
    for user in users:
        auths = (
            await session.execute(select(UserAuth).where(UserAuth.user_id == user.id))
        ).scalars().all()
        by_type = {a.ttype: a for a in auths}
        if consts.UserAuth_Ttype.PASSWORD in by_type and consts.UserAuth_Ttype.EMAIL not in by_type:
            pwd = by_type[consts.UserAuth_Ttype.PASSWORD]
            print(
                f"username={user.username!r} user_id={user.id} "
                f"password_identifier={pwd.identifier!r} password_verified={pwd.ifverified.name}"
            )


async def backfill(
    *,
    username: str,
    email: str,
    dry_run: bool = False,
    mark_verified: bool = True,
) -> None:
    async with open_session() as session:
        user = (
            await session.execute(select(User).where(User.username == username))
        ).scalar_one_or_none()
        if user is None:
            raise SystemExit(f"用户不存在: {username!r}")

        existing_email = (
            await session.execute(
                select(UserAuth).where(
                    UserAuth.ttype == consts.UserAuth_Ttype.EMAIL,
                    UserAuth.identifier == email,
                )
            )
        ).scalar_one_or_none()
        if existing_email and str(existing_email.user_id) != str(user.id):
            raise SystemExit(f"邮箱 {email!r} 已绑定其他用户")

        user_email_auth = (
            await session.execute(
                select(UserAuth).where(
                    UserAuth.user_id == user.id,
                    UserAuth.ttype == consts.UserAuth_Ttype.EMAIL,
                )
            )
        ).scalar_one_or_none()
        if user_email_auth:
            print(f"已有 EMAIL auth: id={user_email_auth.id} identifier={user_email_auth.identifier!r}")
            return

        password_auth = (
            await session.execute(
                select(UserAuth).where(
                    UserAuth.user_id == user.id,
                    UserAuth.ttype == consts.UserAuth_Ttype.PASSWORD,
                )
            )
        ).scalar_one_or_none()

        verified = consts.UserAuth_Ifverified.VERIFIED if mark_verified else consts.UserAuth_Ifverified.UNVERIFIED
        print(
            f"user_id={user.id} username={username!r} -> EMAIL identifier={email!r} "
            f"ifverified={verified.name} dry_run={dry_run}"
        )

        if dry_run:
            return

        repo = UserAuthRepository(session)
        async with transaction(session):
            email_auth = await repo.create_one(
                UserAuthSchema(
                    user_id=user.id,
                    ttype=consts.UserAuth_Ttype.EMAIL,
                    identifier=email,
                    credential=None,
                    ifverified=verified,
                )
            )
            if mark_verified and password_auth is not None:
                await repo.update_one(
                    str(password_auth.id),
                    UserAuthSchema(ifverified=consts.UserAuth_Ifverified.VERIFIED),
                )

        print(f"created EMAIL auth id={email_auth.id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill EMAIL user_auth for legacy users")
    parser.add_argument("--list-missing", action="store_true", help="列出有 PASSWORD 无 EMAIL 的用户")
    parser.add_argument("--username", help="目标用户名")
    parser.add_argument("--email", help="绑定邮箱")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--unverified",
        action="store_true",
        help="EMAIL 记为未验证（默认历史用户直接 VERIFIED）",
    )
    args = parser.parse_args()

    if args.list_missing:
        asyncio.run(_list_missing_wrapper())
        return

    if not args.username or not args.email:
        parser.error("需要 --username 与 --email，或使用 --list-missing")

    asyncio.run(
        backfill(
            username=args.username,
            email=args.email,
            dry_run=args.dry_run,
            mark_verified=not args.unverified,
        )
    )


async def _list_missing_wrapper() -> None:
    async with open_session() as session:
        await list_missing(session)


if __name__ == "__main__":
    main()
