# -*- coding: utf-8 -*-
# @FILE    : api/__init__.py
# @AUTH    : model_creater

from fastapi import APIRouter

# 本模块方法
from .completion import router as completion_router
from .puzzle import router as puzzle_router
from .upload import router as upload_router

router = APIRouter(prefix="/sudoku", tags=["sudoku"])
router.include_router(upload_router, prefix="/upload", tags=["sudoku-upload"])
router.include_router(puzzle_router, prefix="/puzzles", tags=["sudoku-puzzle"])
router.include_router(completion_router, prefix="/completions", tags=["sudoku-completion"])
