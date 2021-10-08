# -*- coding: utf-8 -*-
# @File    : views.py
# @AUTH    : model

import bson
import json
import logging
from typing import Optional, List

from fastapi import FastAPI, APIRouter, Path, Query, Body
from fastapi.param_functions import Depends

from ..schemas import Filter, Pager
from .. import dependencies
from . import schemas
from web import SuccessData
from commons.Helpers.Helper_pagenate import Page

from .utils.password_lock import PasswordLock

router = APIRouter(
    prefix="/passwordlock",
    tags=["password_lock"],
)

logger = logging.getLogger("main.password_lock.views")


@router.get("/{password_lock_id}")
async def get_passwordlock(
    password_lock_id: str = Path(...),
):
    password_lock = await PasswordLock.find(password_lock_id)
    return SuccessData(data=password_lock)


@router.get("/")
async def get_passwordlock_list(
    password_lock: schemas.PasswordLock = Body(...),
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


@router.post("/{passwordlock_id}")
async def copy_passwordlock(
    password_lock_id: str = Path(...),
    password_lock_model: schemas.PasswordLock = Body(...),
):
    password_lock = await PasswordLock.find(password_lock_id)
    copyed_password_lock = await PasswordLock.create(
        password_lock.copy(update=password_lock_model.dict(exclude_defaults=True)),
    )
    return SuccessData(id=copyed_password_lock.id)


@router.post("/")
async def create_passwordlock(
    password_lock_model: schemas.PasswordLock = Body(...),
):
    password_lock = await PasswordLock.create(
        password_lock_model.dict(),
    )
    return SuccessData(id=password_lock.id)


@router.put("/{passwordlock_id}")
async def change_passwordlock(
    password_lock_id: str = Path(...),
    password_lock_model: schemas.PasswordLock = Body(...),
):
    password_lock = await PasswordLock.find_and_update(
        password_lock_id,
        password_lock_model.dict(),
    )
    return SuccessData(id=password_lock.id)


@router.delete("/{passwordlock_id}")
async def delete_passwordlick(
    password_lock_id: str = Path(...),
):
    count = await PasswordLock.find_and_delete(password_lock_id)
    return SuccessData(count=count)


@router.patch("/{passwordlock_id}")
async def modify_passwordlick(
    password_lock_id: str = Path(...),
    password_lock_model: schemas.PasswordLock = Body(...),
):
    password_lock = await PasswordLock.find_and_update(
        password_lock_id,
        password_lock_model.dict(exclude_defaults=True),
    )
    return SuccessData(id=password_lock.id)
