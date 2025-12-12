# -*- coding: utf-8 -*-

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

import core
from web.handlers.unknown_exception_handler import unknown_exception_handler
from web.handlers.unknown_http_handler import unknown_http_handler

from apps import api_router

logger = logging.getLogger("main")

app = FastAPI(
    debug=core.config.DEBUG,
    openapi_url="/api/v1/openapi.json",
)

app.add_exception_handler(HTTPException, unknown_http_handler)
app.add_exception_handler(Exception, unknown_exception_handler)

app.include_router(router=api_router)
