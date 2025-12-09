# -*- coding: utf-8 -*-
# @File    : import_mongodb_data.py
# @AUTH    : code_creater
"""
从MongoDB导出的JSON文件批量导入到MySQL数据库
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from bson import ObjectId
from sqlalchemy.ext.asyncio import AsyncSession

from apps.password_lock.models.password_lock import PasswordLock
from apps.system.models.user import User
from apps.system.models.user_auth import UserAuth
from apps.upload.models.file_info import FileInfo
from apps.wechat.models.wechat_msg import WechatMsg
from mysqlengine import SessionLocal, baseModel

# 文件名到模型类的映射
FILE_MODEL_MAP = {
    "user.json": User,
    "user_auth.json": UserAuth,
    "file_info.json": FileInfo,
    "password_lock.json": PasswordLock,
    "wechat_msg.json": WechatMsg,
}


def parse_mongodb_value(value: Any) -> Any:
    """
    解析MongoDB导出的特殊格式值
    支持 $oid 和 $date 格式
    """
    if isinstance(value, dict):
        if "$oid" in value:
            return ObjectId(value["$oid"])
        elif "$date" in value:
            # 解析ISO格式日期字符串
            date_str = value["$date"]
            if isinstance(date_str, str):
                try:
                    # 处理ISO格式日期字符串
                    # 移除末尾的Z并转换为datetime
                    if date_str.endswith("Z"):
                        date_str = date_str[:-1] + "+00:00"
                    elif "+" not in date_str and "-" in date_str:
                        # 如果没有时区信息，添加UTC时区
                        if not date_str.endswith("+00:00"):
                            date_str = date_str + "+00:00"
                    return datetime.fromisoformat(date_str)
                except ValueError as e:
                    # 如果解析失败，尝试其他格式
                    try:
                        # 尝试解析为时间戳（毫秒）
                        if isinstance(date_str, (int, float)):
                            return datetime.fromtimestamp(date_str / 1000)
                    except Exception:
                        pass
                    print(f"警告: 无法解析日期格式: {date_str}, 错误: {e}")
                    return datetime.now()  # 使用当前时间作为默认值
            elif isinstance(date_str, (int, float)):
                # 处理时间戳（毫秒）
                return datetime.fromtimestamp(date_str / 1000)
            return date_str
        else:
            # 递归处理嵌套字典
            return {k: parse_mongodb_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [parse_mongodb_value(item) for item in value]
    return value


def transform_mongodb_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    将MongoDB记录转换为MySQL模型格式
    字段映射：
    - _id -> id
    - created -> create_at
    - updated -> update_at
    """
    transformed = {}

    for key, value in record.items():
        # 字段名映射
        if key == "_id":
            transformed["id"] = parse_mongodb_value(value)
        elif key == "created":
            transformed["create_at"] = parse_mongodb_value(value)
        elif key == "updated":
            transformed["update_at"] = parse_mongodb_value(value)
        else:
            # 其他字段直接转换，但需要解析MongoDB特殊格式
            transformed[key] = parse_mongodb_value(value)

    return transformed


async def import_json_file(
    file_path: Path, model_class: type[baseModel], db: AsyncSession, batch_size: int = 100
) -> int:
    """
    导入单个JSON文件到数据库

    Args:
        file_path: JSON文件路径
        model_class: 对应的模型类
        db: 数据库会话
        batch_size: 批量插入大小

    Returns:
        导入的记录数
    """
    print(f"\n开始导入文件: {file_path.name}")
    print("-" * 50)

    # 读取JSON文件
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误: 无法读取文件 {file_path.name}: {str(e)}")
        return 0

    if not isinstance(data, list):
        print(f"警告: {file_path.name} 不是数组格式，跳过")
        return 0

    total_records = len(data)
    print(f"文件包含 {total_records} 条记录")

    # 批量处理
    imported_count = 0
    skipped_count = 0

    for i in range(0, total_records, batch_size):
        batch = data[i : i + batch_size]
        instances = []

        for record in batch:
            try:
                # 转换记录格式
                transformed = transform_mongodb_record(record)

                # 过滤掉模型中不存在的字段
                model_columns = {col.name for col in model_class.__table__.columns}
                filtered = {k: v for k, v in transformed.items() if k in model_columns}

                # 创建模型实例
                instance = model_class(**filtered)
                instances.append(instance)
            except Exception as e:
                record_id = (
                    record.get("_id", {}).get("$oid", "unknown")
                    if isinstance(record.get("_id"), dict)
                    else record.get("_id", "unknown")
                )
                print(f"警告: 跳过记录 {record_id}: {str(e)}")
                skipped_count += 1
                continue

        if instances:
            try:
                # 批量添加
                db.add_all(instances)
                await db.flush()
                imported_count += len(instances)
                print(f"进度: {imported_count}/{total_records} 条记录已导入")
            except Exception as e:
                print(f"错误: 批量插入失败: {str(e)}")
                # 回滚当前批次
                await db.rollback()
                # 尝试逐条插入
                for instance in instances:
                    try:
                        db.add(instance)
                        await db.flush()
                        imported_count += 1
                    except Exception as inner_e:
                        print(f"警告: 单条插入失败 (ID: {getattr(instance, 'id', 'unknown')}): {str(inner_e)}")
                        skipped_count += 1
                        await db.rollback()

    print(f"\n文件 {file_path.name} 导入完成: 成功 {imported_count} 条, 跳过 {skipped_count} 条")
    return imported_count


async def import_all_files(data_dir: Path, batch_size: int = 100, skip_existing: bool = True):
    """
    导入data目录下的所有JSON文件

    Args:
        data_dir: 数据文件目录
        batch_size: 批量插入大小
        skip_existing: 是否跳过已存在的记录（基于ID）
    """
    if not data_dir.exists():
        print(f"错误: 目录不存在: {data_dir}")
        return

    # 获取所有JSON文件
    json_files = list(data_dir.glob("*.json"))

    if not json_files:
        print(f"警告: 在 {data_dir} 中未找到JSON文件")
        return

    print(f"找到 {len(json_files)} 个JSON文件")

    async with SessionLocal() as db:
        total_imported = 0

        for json_file in json_files:
            file_name = json_file.name

            # 查找对应的模型类
            if file_name not in FILE_MODEL_MAP:
                print(f"警告: 未找到 {file_name} 对应的模型类，跳过")
                continue

            model_class = FILE_MODEL_MAP[file_name]

            try:
                # 导入文件
                count = await import_json_file(json_file, model_class, db, batch_size)
                total_imported += count

                # 提交当前文件的更改
                await db.commit()
                print(f"✓ {file_name} 提交成功\n")
            except Exception as e:
                print(f"错误: 导入 {file_name} 时发生错误: {str(e)}")
                await db.rollback()
                print(f"✗ {file_name} 已回滚\n")

        print(f"=" * 50)
        print(f"导入完成! 总共导入 {total_imported} 条记录")


async def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    print("=" * 50)
    print("MongoDB数据批量导入工具")
    print("=" * 50)
    print(f"数据目录: {data_dir}")
    print()

    # 导入所有文件
    await import_all_files(data_dir, batch_size=100)


if __name__ == "__main__":
    asyncio.run(main())
