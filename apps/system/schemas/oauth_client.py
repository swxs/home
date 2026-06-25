# -*- coding: utf-8 -*-
# @FILE    : schemas/oauth_client.py
# @AUTH    : code_creater

from typing import Optional

from fastapi import Query

from web.custom_types import objectId
from web.schemas import BaseSchema

# 本模块方法
from .. import consts


# 说明：OAuthClientSchema 作为字段基类保留，并被作为「创建/查询/更新载荷」在 oauth 等处复用。
class OAuthClientSchema(BaseSchema):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    client_name: Optional[str] = None
    redirect_uri: Optional[str] = None
    user_id: Optional[objectId] = None
    is_active: Optional[consts.OAuthClient_IsActive] = None


class OAuthClientFilter(OAuthClientSchema):
    """列表查询过滤条件。"""


class OAuthClientUpdate(OAuthClientSchema):
    """更新入参。"""


class OAuthClientOut(OAuthClientSchema):
    """输出 DTO（注意：调用方需自行 pop client_secret，沿用现有行为）。"""


class OAuthClientCreateSchema(BaseSchema):
    """创建OAuth客户端时的Schema，不包含client_id和client_secret（由系统生成）"""

    client_name: str
    redirect_uri: str
    user_id: Optional[objectId] = None


class OAuthClientResponseSchema(BaseSchema):
    """返回给客户端的Schema，包含client_id和client_secret"""

    client_id: str
    client_secret: str
    client_name: str
    redirect_uri: str
    user_id: Optional[objectId] = None
    is_active: consts.OAuthClient_IsActive


async def get_oauth_client_filter(
    client_id: Optional[str] = Query(None),
    client_name: Optional[str] = Query(None),
    redirect_uri: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
) -> OAuthClientFilter:
    params = {}
    if client_id is not None:
        params["client_id"] = client_id
    if client_name is not None:
        params["client_name"] = client_name
    if redirect_uri is not None:
        params["redirect_uri"] = redirect_uri
    if user_id is not None:
        params["user_id"] = user_id
    if is_active is not None:
        params["is_active"] = is_active

    return OAuthClientFilter(**params)
