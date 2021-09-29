# -*- coding: utf-8 -*-
# @File    : views.py
# @AUTH    : model

import bson
import json
import logging
from typing import Optional, List

from fastapi import FastAPI, Path, Query, Body
from fastapi.param_functions import Depends

from .. import reg
from ..schemas import Filter, Pager
from .. import dependencies
from . import schemas
from web import SuccessData
from commons.Helpers.Helper_pagenate import Page

from .utils.PasswordLock import PasswordLock

app = FastAPI()
logger = logging.getLogger("main.password_lock.views")


@app.get("/passwordlock/{password_lock_id}")
async def get_passwordlock(
    self,
    password_lock_id: str = Path(..., regex=reg.COLUMN_ID),
):
    password_lock = await PasswordLock.find(password_lock_id)
    return SuccessData(data=password_lock)


@app.get("/passwordlock")
async def get_passwordlock_list(
    self,
    password_lock: schemas.PasswordLock = Query(...),
    filter_: Filter = Depends(dependencies.get_filter),
    pager: Pager = Depends(dependencies.get_pager),
):
    password_lock_list = PasswordLock.search(
        password_lock.dict(exclude_unset=True),
        filter_,
        skip=pager.skip,
        limit=pager.limit,
    )
    return SuccessData(data=password_lock_list, info=pager)


@app.post("/passwordlock/{passwordlock_id}")
async def copy_passwordlock(
    self,
    password_lock_id: str = Path(..., regex=reg.COLUMN_ID),
    password_lock_model: PasswordLock = Body(...),
):
    password_lock = await PasswordLock.find(password_lock_id)
    copyed_password_lock = await PasswordLock.create(
        password_lock.copy(update=password_lock_model.dict(exclude_defaults=True)),
    )
    return SuccessData(id=copyed_password_lock.id)


@app.post("/passwordlock")
async def create_passwordlock(
    self,
    password_lock: PasswordLock = Body(...),
):
    password_lock = await PasswordLock.create(
        password_lock,
    )
    return SuccessData(id=password_lock.id)


@app.put("/passwordlock/{passwordlock_id}")
async def change_passwordlock(
    self,
    password_lock_id: str = Path(..., regex=reg.COLUMN_ID),
    password_lock_model: PasswordLock = Body(...),
):
    password_lock = await PasswordLock.find_and_update(
        password_lock_id,
        password_lock_model.dict(),
    )
    return SuccessData(id=password_lock.id)


@app.delete("/passwordlock/{passwordlock_id}")
async def delete_passwordlick(
    self,
    password_lock_id: str = Path(..., regex=reg.COLUMN_ID),
):
    count = await PasswordLock.find_and_delete(password_lock_id)
    return SuccessData(count=count)


@app.patch("/passwordlock/{passwordlock_id}")
async def modify_passwordlick(
    self,
    password_lock_id: str = Path(..., regex=reg.COLUMN_ID),
    password_lock_model: PasswordLock = Body(...),
):
    password_lock = await PasswordLock.find_and_update(
        password_lock_id,
        password_lock_model.dict(exclude_defaults=True),
    )
    return SuccessData(id=password_lock.id)
