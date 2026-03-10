# -*- coding: utf-8 -*-
# @FILE    : utils/sudoku_validator.py
# @AUTH    : code_creater

"""数独网格合法性校验：行、列、宫均为 1-9 不重复。"""


def is_valid_sudoku_grid(grid: str) -> bool:
    """
    校验 81 位字符串是否为合法数独解（每行、每列、每宫 1-9 各出现一次）。

    Args:
        grid: 长度 81，仅含 '1'-'9'

    Returns:
        True 表示合法
    """
    if not grid or len(grid) != 81:
        return False
    valid_chars = set("123456789")
    for c in grid:
        if c not in valid_chars:
            return False

    def cell(i: int, j: int) -> str:
        return grid[i * 9 + j]

    # 行
    for i in range(9):
        row = [cell(i, j) for j in range(9)]
        if len(set(row)) != 9:
            return False
    # 列
    for j in range(9):
        col = [cell(i, j) for i in range(9)]
        if len(set(col)) != 9:
            return False
    # 宫（3x3）
    for bi in range(3):
        for bj in range(3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(cell(bi * 3 + i, bj * 3 + j))
            if len(set(block)) != 9:
                return False
    return True
