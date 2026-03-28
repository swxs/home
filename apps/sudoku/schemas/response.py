# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import List, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .sudoku_completion import SudokuCompletionItemSchema
from .sudoku_puzzle import SudokuPuzzleSchema, SudokuUploadPreviewData


class SudokuPuzzleResponse(TypedDict):
    data: SudokuPuzzleSchema


class SudokuUploadPreviewResponse(TypedDict):
    data: SudokuUploadPreviewData


class SudokuPuzzleSearchResponse(TypedDict):
    data: List[SudokuPuzzleSchema]
    pagination: PaginationSchema


class SudokuCompletionSearchResponse(TypedDict):
    data: List[SudokuCompletionItemSchema]
    pagination: PaginationSchema
