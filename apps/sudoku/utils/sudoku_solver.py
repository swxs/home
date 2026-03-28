# -*- coding: utf-8 -*-
# @File    : utils/sudoku_solver.py
# @AUTH    : code_creater

"""数独题目规范化与唯一解求解。"""

from __future__ import annotations


def normalize_puzzle_input(raw: str) -> str:
    """
    从粘贴文本提取 81 位题目串：空白忽略；. _ 视为 0；仅允许 0-9。

    Raises:
        ValueError: 长度非 81 或含非法字符
    """
    if raw is None:
        raise ValueError("题目内容不能为空")
    out: list[str] = []
    for c in str(raw):
        if c in " \t\n\r":
            continue
        if c in "._":
            out.append("0")
        elif c in "0123456789":
            out.append(c)
        else:
            raise ValueError(f"非法字符: {c!r}（仅支持 0-9、空格、换行、.、_）")
    if len(out) != 81:
        raise ValueError(f"有效格子数须为 81，当前为 {len(out)}")
    return "".join(out)


def _partial_puzzle_valid(puzzle: str) -> bool:
    """已填数字（非 0）在行、列、宫内是否无重复。"""
    grid = [puzzle[i : i + 9] for i in range(0, 81, 9)]

    def box_chars(br: int, bc: int) -> list[str]:
        chars: list[str] = []
        for r in range(br * 3, br * 3 + 3):
            for c in range(bc * 3, bc * 3 + 3):
                ch = grid[r][c]
                if ch != "0":
                    chars.append(ch)
        return chars

    for i in range(9):
        row = [c for c in grid[i] if c != "0"]
        if len(row) != len(set(row)):
            return False
        col = [grid[r][i] for r in range(9) if grid[r][i] != "0"]
        if len(col) != len(set(col)):
            return False
    for br in range(3):
        for bc in range(3):
            b = box_chars(br, bc)
            if len(b) != len(set(b)):
                return False
    return True


def solve_unique_solution(puzzle: str) -> str:
    """
    求唯一解。若无解、多解则抛出 ValueError。

    Args:
        puzzle: 已规范化的 81 位串，0 表示空格

    Returns:
        81 位答案串（仅含 1-9）
    """
    if len(puzzle) != 81:
        raise ValueError("puzzle 须为 81 位")
    if "0" not in puzzle:
        raise ValueError("题目至少需要有一个空格（0）")
    if not _partial_puzzle_valid(puzzle):
        raise ValueError("题目中已填数字存在重复，不符合数独规则")

    cells: list[int] = [int(c) for c in puzzle]
    first_solution: list[str] | None = None
    solution_count = 0

    def idx(r: int, c: int) -> int:
        return r * 9 + c

    def neighbors_used(pos: int) -> set[int]:
        used: set[int] = set()
        r, c = pos // 9, pos % 9
        br, bc = r // 3, c // 3
        for j in range(9):
            v = cells[idx(r, j)]
            if v:
                used.add(v)
        for i in range(9):
            v = cells[idx(i, c)]
            if v:
                used.add(v)
        for i in range(br * 3, br * 3 + 3):
            for j in range(bc * 3, bc * 3 + 3):
                v = cells[idx(i, j)]
                if v:
                    used.add(v)
        return used

    def dfs() -> None:
        nonlocal solution_count, first_solution
        if solution_count >= 2:
            return
        try:
            pos = cells.index(0)
        except ValueError:
            solution_count += 1
            if first_solution is None:
                first_solution = [str(x) for x in cells]
            return
        for d in range(1, 10):
            if d in neighbors_used(pos):
                continue
            cells[pos] = d
            dfs()
            if solution_count >= 2:
                cells[pos] = 0
                return
            cells[pos] = 0

    dfs()

    if solution_count == 0:
        raise ValueError("该题目无解")
    if solution_count >= 2:
        raise ValueError("该题目存在多个解，请提供唯一解题目")
    assert first_solution is not None
    return "".join(first_solution)
