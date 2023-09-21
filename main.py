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
from web.exceptions.http_404_not_found_exception import Http404NotFoundException
from web.handlers.unknown_exception_handler import unknown_exception_handler
from web.handlers.unknown_http_handler import unknown_http_handler
from web.response import exception

logger = logging.getLogger("main")

app = FastAPI(
    debug=core.config.DEBUG,
)


@app.on_event("startup")
async def event_startup():
    logging.info("connect to database....")
    core.mongodb_database.client = AsyncIOMotorClient(core.config.MONGODB_URI)
    # 检查索引
    logging.info(f"Connected to database!")


@app.on_event("shutdown")
async def event_shutdown():
    logging.info(f"close mongodb connection....")
    core.mongodb_database.client.close()
    logging.info("connection to mongodb has been closed!")


app.add_exception_handler(HTTPException, unknown_http_handler)
app.add_exception_handler(Exception, unknown_exception_handler)

app.include_router(router=api_router)
