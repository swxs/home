# -*- coding: utf-8 -*-
"""将 user_auth 表中 PASSWORD 类型的明文 credential 迁移为 bcrypt 哈希。

用法（在能连上数据库的环境，如 home 容器内）：
  uv run python scripts/migrate_password_to_bcrypt.py
  uv run python scripts/migrate_password_to_bcrypt.py --dry-run
  uv run python scripts/migrate_password_to_bcrypt.py --plaintext swxs321jxrewq
"""

import argparse
import asyncio

from sqlalchemy import select

from apps.system import consts
from apps.system.models.user_auth import UserAuth
from apps.system.utils.password import hash_password
from mysqlengine import SessionLocal
from web.dependencies.transaction import transaction


def _is_bcrypt(credential: str) -> bool:
    return bool(credential) and credential.startswith(("$2a$", "$2b$", "$2y$"))


async def migrate(*, dry_run: bool = False, plaintext_filter: str | None = None) -> None:
    migrated = 0
    skipped = 0

    async with SessionLocal() as db:
        result = await db.execute(select(UserAuth).where(UserAuth.ttype == consts.UserAuth_Ttype.PASSWORD))
        rows = list(result.scalars().all())

        async with transaction(db):
            for row in rows:
                cred = row.credential or ""
                if _is_bcrypt(cred):
                    skipped += 1
                    continue
                if plaintext_filter is not None and cred != plaintext_filter:
                    skipped += 1
                    continue
                if not cred:
                    skipped += 1
                    continue

                new_hash = hash_password(cred)
                print(f"migrate id={row.id} identifier={row.identifier!r} plain_len={len(cred)}")
                if not dry_run:
                    row.credential = new_hash
                migrated += 1

    action = "would migrate" if dry_run else "migrated"
    print(f"Done: {action}={migrated}, skipped={skipped}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate plaintext PASSWORD credentials to bcrypt")
    parser.add_argument("--dry-run", action="store_true", help="只打印，不写库")
    parser.add_argument(
        "--plaintext",
        default=None,
        help="仅迁移指定明文密码（默认迁移所有非 bcrypt 记录）",
    )
    args = parser.parse_args()
    asyncio.run(migrate(dry_run=args.dry_run, plaintext_filter=args.plaintext))


if __name__ == "__main__":
    main()
