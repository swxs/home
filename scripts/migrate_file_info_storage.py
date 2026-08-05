"""迁移历史 FileInfo 归属并将 OSS 对象重刷为 MD5 + size key。

用法：
  uv run python scripts/migrate_file_info_storage.py --user-id 64f000000000000000000001 --dry-run
  uv run python scripts/migrate_file_info_storage.py --user-id 64f000000000000000000001

脚本可幂等重跑。只有新对象校验成功且数据库归属已提交后，才会删除旧对象。
"""

import argparse
import asyncio
import sys
from dataclasses import dataclass
from pathlib import Path

from bson import ObjectId
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from commons.Helpers import oss2_helper  # noqa: E402
from mysqlengine import SessionLocal  # noqa: E402

# 脚本允许直接从仓库根目录运行。
from apps.upload.storage import build_object_key  # noqa: E402


@dataclass
class MigrationStats:
    migrated: int = 0
    skipped: int = 0
    failed: int = 0


def build_legacy_object_key(file_id: str) -> str:
    normalized_id = file_id.lower()
    return f"{normalized_id[:4]}/{normalized_id[4:]}"


async def _column_exists(db, column_name: str) -> bool:
    result = await db.execute(
        text(
            """
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'file_info'
              AND COLUMN_NAME = :column_name
            """
        ),
        {"column_name": column_name},
    )
    return bool(result.scalar())


async def _index_rows(db) -> list[dict]:
    result = await db.execute(text("SHOW INDEX FROM file_info"))
    return [dict(row) for row in result.mappings().all()]


async def _ensure_target_user(db, user_id: str) -> bytes:
    try:
        raw_user_id = ObjectId(user_id).binary
    except Exception as exc:
        raise ValueError("--user-id 必须是 24 位 ObjectId 十六进制字符串") from exc

    result = await db.execute(
        text("SELECT COUNT(*) FROM `user` WHERE id = :user_id"),
        {"user_id": raw_user_id},
    )
    if not result.scalar():
        raise ValueError(f"指定用户不存在: {user_id}")
    return raw_user_id


async def _ensure_nullable_user_id(db) -> None:
    if await _column_exists(db, "user_id"):
        return
    await db.execute(
        text(
            "ALTER TABLE file_info "
            "ADD COLUMN user_id BINARY(12) NULL COMMENT '所属用户ID' AFTER id"
        )
    )
    await db.commit()


async def _load_rows(db, *, has_user_id: bool):
    user_column = "user_id" if has_user_id else "NULL AS user_id"
    result = await db.execute(
        text(
            f"SELECT id, file_id, file_size, {user_column} "  # noqa: S608 - 列名由常量决定
            "FROM file_info ORDER BY create_at, id"
        )
    )
    return list(result.mappings().all())


def _validate_size(oss_helper, key: str, expected_size: int) -> None:
    _, _, actual_size = oss_helper.get_file_meta(key)
    if actual_size != expected_size:
        raise ValueError(
            f"OSS 对象大小不一致: key={key}, expected={expected_size}, actual={actual_size}"
        )


async def _finalize_schema(db) -> None:
    null_count = (
        await db.execute(text("SELECT COUNT(*) FROM file_info WHERE user_id IS NULL"))
    ).scalar()
    if null_count:
        raise RuntimeError(f"仍有 {null_count} 条 FileInfo 未设置 user_id，不能收紧约束")

    indexes = await _index_rows(db)
    grouped: dict[str, list[dict]] = {}
    for row in indexes:
        grouped.setdefault(row["Key_name"], []).append(row)

    for name, rows in grouped.items():
        ordered = sorted(rows, key=lambda item: item["Seq_in_index"])
        columns = [item["Column_name"] for item in ordered]
        if name != "PRIMARY" and rows[0]["Non_unique"] == 0 and columns == ["file_id"]:
            await db.execute(text(f"ALTER TABLE file_info DROP INDEX `{name}`"))

    indexes = await _index_rows(db)
    names = {row["Key_name"] for row in indexes}
    if "uq_file_info_user_content" not in names:
        await db.execute(
            text(
                "ALTER TABLE file_info ADD CONSTRAINT uq_file_info_user_content "
                "UNIQUE (user_id, file_id, file_size)"
            )
        )
    if "idx_file_info_user_id" not in names:
        await db.execute(text("CREATE INDEX idx_file_info_user_id ON file_info (user_id)"))
    if "idx_file_info_content" not in names:
        await db.execute(
            text("CREATE INDEX idx_file_info_content ON file_info (file_id, file_size)")
        )

    await db.execute(
        text(
            "ALTER TABLE file_info MODIFY COLUMN "
            "user_id BINARY(12) NOT NULL COMMENT '所属用户ID'"
        )
    )
    await db.commit()


async def migrate(
    *,
    user_id: str,
    dry_run: bool = False,
    oss_helper=oss2_helper,
) -> MigrationStats:
    stats = MigrationStats()
    async with SessionLocal() as db:
        raw_user_id = await _ensure_target_user(db, user_id)
        has_user_id = await _column_exists(db, "user_id")
        rows = await _load_rows(db, has_user_id=has_user_id)

        if dry_run:
            print("DRY RUN: 不修改数据库或 OSS")
        else:
            await _ensure_nullable_user_id(db)

        for row in rows:
            row_id = row["id"]
            file_id = row["file_id"].lower()
            file_size = int(row["file_size"])
            current_user_id = row["user_id"]
            old_key = build_legacy_object_key(file_id)
            new_key = build_object_key(file_id, file_size)

            if current_user_id not in (None, raw_user_id):
                print(f"FAILED id={row_id}: 已归属其他用户")
                stats.failed += 1
                continue

            try:
                new_exists = oss_helper.exists(new_key)
                old_exists = oss_helper.exists(old_key)
                if new_exists:
                    _validate_size(oss_helper, new_key, file_size)
                elif not old_exists:
                    raise ValueError(f"新旧 OSS 对象均不存在: {old_key}")
                else:
                    _validate_size(oss_helper, old_key, file_size)
                    if not dry_run:
                        oss_helper.copy(old_key, new_key)
                        _validate_size(oss_helper, new_key, file_size)

                if dry_run:
                    action = "would migrate" if current_user_id is None else "would verify"
                    print(f"{action} id={row_id} {old_key} -> {new_key} user={user_id}")
                    stats.migrated += int(current_user_id is None)
                    stats.skipped += int(current_user_id is not None)
                    continue

                if current_user_id is None:
                    await db.execute(
                        text("UPDATE file_info SET user_id = :user_id WHERE id = :id"),
                        {"user_id": raw_user_id, "id": row_id},
                    )
                    await db.commit()
                    stats.migrated += 1
                else:
                    stats.skipped += 1

                if old_exists:
                    oss_helper.delete(old_key)
                print(f"OK id={row_id} key={new_key} user={user_id}")
            except Exception as exc:
                await db.rollback()
                stats.failed += 1
                print(f"FAILED id={row_id}: {exc}")

        if not dry_run and stats.failed == 0:
            await _finalize_schema(db)

    action = "would migrate" if dry_run else "migrated"
    print(
        f"Done: {action}={stats.migrated}, skipped={stats.skipped}, failed={stats.failed}"
    )
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate FileInfo ownership and OSS object keys"
    )
    parser.add_argument("--user-id", required=True, help="历史文件归属的 User ObjectId")
    parser.add_argument("--dry-run", action="store_true", help="仅校验和打印，不写库或 OSS")
    args = parser.parse_args()
    asyncio.run(migrate(user_id=args.user_id, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
