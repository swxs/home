# -*- coding: utf-8 -*-
# @File    : fields.py
# @AUTH    : Gorden
# @Time    : 2021/9/15 01:04
import codecs
from enum import IntEnum
from typing import Optional, Type

import sqlalchemy
from sqlalchemy import TypeDecorator


class IntEnumType(TypeDecorator):
    """
    IntEnum类型数据(枚举整数)
    需在-128 <= v <= 127之间

    Example:
        from enum import IntEnum

        class StatusEnum(IntEnum):
            PENDING = 0
            ACTIVE = 1
            INACTIVE = 2
            DELETED = -1

        # 在模型中使用 - 方式1: 直接实例化
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            status = Column(IntEnumType(choice=StatusEnum))

        # 在模型中使用 - 方式2: 使用 mapped_column (推荐)
        class User(Base):
            __tablename__ = 'users'
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            status: Mapped[int] = mapped_column(
                IntEnumType(choice=StatusEnum),
                default=StatusEnum.ACTIVE,
                comment="状态"
            )

        # 使用示例
        user = User()
        user.status = StatusEnum.ACTIVE  # 使用枚举值
        user.status = 1  # 也可以直接使用整数值

        # 验证会确保值在枚举范围内
        # user.status = 999  # 会抛出 ValueError
    """

    impl = sqlalchemy.types.SMALLINT  # tinyint为mysql独有的，所以这里采用smallint
    cache_ok = False  # 值为None不能生成cache_key，且会出现警告。调整为False

    def __init__(self, choice: Type[IntEnum], *args, **kwargs):
        """
        初始化 IntEnumType

        Args:
            choice: IntEnum 的子类，用于定义允许的枚举值
            *args, **kwargs: 传递给父类的其他参数
        """
        self._choice = choice
        self._choice_values = None
        self.__validate_choice()
        super(IntEnumType, self).__init__(*args, **kwargs)

    def __validate_choice(self):
        if self._choice is None:
            return True

        # 检查是否是 IntEnum 类型
        if not issubclass(self._choice, IntEnum):
            raise ValueError("'choice' must be an IntEnum class (subclass of enum.IntEnum).")

        # 提取所有枚举值
        self._choice_values = [member.value for member in self._choice]

        if not self._choice_values:
            raise ValueError("'choice' IntEnum cannot be empty.")

        # 验证所有值都在有效范围内
        for v in self._choice_values:
            if not isinstance(v, int):
                raise ValueError("'choice' IntEnum values must be all int type.")
            if not (-128 <= v <= 127):  # signed tinyint max size
                raise ValueError(f"'choice' IntEnum values must be in [-128, 127], got {v}.")

        return True

    def __validate(self, value):
        if value is None:
            return True

        # 如果传入的是枚举成员，提取其值
        if isinstance(value, self._choice):
            value = value.value

        try:
            value = int(value)
        except (ValueError, TypeError):
            raise TypeError("Field value must be int type or IntEnum member.")

        if self._choice_values is not None and value not in self._choice_values:
            raise ValueError(f"value must be one of {self._choice_values} (from {self._choice.__name__}).")

        return True

    def process_bind_param(self, value, dialect):
        self.__validate(value)
        if value is None:
            return None
        # 如果传入的是枚举成员，提取其值
        if isinstance(value, self._choice):
            return value.value
        return int(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # 尝试将数据库值转换回枚举成员
        int_value = int(value)
        try:
            return self._choice(int_value)
        except ValueError:
            # 如果值不在枚举中，返回整数值
            return int_value
