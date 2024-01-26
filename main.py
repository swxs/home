# -*- coding: utf-8 -*-

import os
import sys
import typing
import logging
import multiprocessing

import click
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.exceptions import HTTPException

import core
from apps import api_router
from web.handlers.unknown_exception_handler import unknown_exception_handler
from web.handlers.unknown_http_handler import unknown_http_handler

logger = logging.getLogger("main")

app = FastAPI(
    debug=core.config.DEBUG,
)


@app.on_event("startup")
async def event_startup():
    # 扫描所有model, 实例化manager\memorizer , 触发manager\memorizer的初始化方法
    logging.info("app startup begin....")

    logging.info("app startup finish....")


@app.on_event("shutdown")
async def event_shutdown():
    logging.info("app shutdown begin....")

    logging.info("app shutdown finish....")


app.add_exception_handler(HTTPException, unknown_http_handler)
app.add_exception_handler(Exception, unknown_exception_handler)

app.include_router(router=api_router)
