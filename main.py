# -*- coding: utf-8 -*-

import os
import sys
import typing
import click
import logging
import logging.config
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import settings


logging.config.fileConfig('logging.ini')
logger = logging.getLogger("main")


@click.command()
@click.option(
    '-m',
    '--mode',
    required=True,
    type=click.Choice(['WEB', 'RPC'], case_sensitive=False),
    default='WEB',
    show_default=True,
)
@click.option(
    '-t',
    '--task',
    required=True,
    type=click.Choice(['START', 'STOP'], case_sensitive=False),
    default='START',
    show_default=True,
)
@click.argument('ports', nargs=1, type=int)
def main(mode, task, ports):
    if mode == "WEB" and task == "START":
        from web import main as web_main

        if not ports:
            ports = settings.SITE_PORT

        web_main.main(ports)


# if __name__ == "__main__":
#     main()

import uvicorn
from fastapi import Depends, FastAPI

from apps.PasswordLock.handlers import router

app = FastAPI()

from motor.motor_asyncio import AsyncIOMotorClient
from settings import database


@app.on_event("startup")
async def event_startup():
    logging.info("connect to database....")
    database.client = AsyncIOMotorClient()
    logging.info("Connected to database!")


@app.on_event("shutdown")
async def event_shutdown():
    logging.info("close mongodb connection....")
    database.client.close()
    logging.info("connection to mongodb has been closed!")


app.include_router(router)


if __name__ == '__main__':
    # uvicorn.run(app, host="127.0.0.1", port=8895)
    uvicorn.run("main:app", host="127.0.0.1", port=8895)
    # uvicorn.run("main:app", host="127.0.0.1", port=8895, reload=True)
