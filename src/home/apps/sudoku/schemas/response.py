# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import List, TypedDict

from home.web.schemas.pagination import PaginationSchema

# 本模块方法
from .sudoku_completion import SudokuCompletionItemSchema
from .sudoku_puzzle import SudokuPuzzleOut, SudokuUploadPreviewData


class SudokuPuzzleResponse(TypedDict):
    data: SudokuPuzzleOut


class SudokuUploadPreviewResponse(TypedDict):
    data: SudokuUploadPreviewData


class SudokuPuzzleSearchResponse(TypedDict):
    data: List[SudokuPuzzleOut]
    pagination: PaginationSchema


class SudokuCompletionSearchResponse(TypedDict):
    data: List[SudokuCompletionItemSchema]
    pagination: PaginationSchema
