# -*- coding: utf-8 -*-

import os
import sys
import typing
import click
import uvicorn
import logging
import multiprocessing
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

import core
from apps.password_lock.api import router as password_lock_router

logger = logging.getLogger("main")

app = FastAPI()


@app.on_event("startup")
async def event_startup():
    logging.info("connect to database....")
    core.mongodb_database.client = AsyncIOMotorClient(core.config.MONGODB_URI)
    logging.info(f"Connected to database!")


@app.on_event("shutdown")
async def event_shutdown():
    logging.info(f"close mongodb connection....")
    core.mongodb_database.client.close()
    logging.info("connection to mongodb has been closed!")


app.include_router(prefix="/api", router=password_lock_router)
