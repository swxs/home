# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

import json
from tornado.web import url
from web.web import BaseHandler
from web.consts import undefined
from web.result import SuccessData
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from commons import jwt_utils
from commons.encrypt import decrypt
from common.Utils.log_utils import getLogger
from ..utils.User import User, user_schema

log = getLogger("views/user")


class AuthTokenHandler(BaseHandler):
    @render
    async def post(self):
        user_name = self.get_argument('user_name')
        password = self.get_argument('password')

        if not user_name:
            raise ValidationError(
                ValidationError.UserNameEmpty, 'user_name is empty.')
        if not password:
            raise ValidationError(
                ValidationError.PwdEmpty, 'password is empty.')

        jwt_data = {}

        if org_code:
            organization = await OrganizationDAO.find_one(dict(
                code=org_code, status=ORGANIZATION_STATUS_ACTIVATED))
            if not organization:
                raise AuthorizationError(
                    AuthorizationError.OrgNotExists, msg='organization code not exist.')
            if organization.expiryDT:
                expire = organization.expiryDT
                expire = date(year=expire.year,
                              month=expire.month, day=expire.day)
                if date.today() > expire:
                    raise AuthorizationError(
                        AuthorizationError.OrgExpire, msg=str(expire))
                jwt_data['org_exp'] = str(expire)
            org_id = organization.oid
            jwt_data['org_code'] = organization.code
            jwt_data['org_id'] = str(org_id)

        user = await UserDAO.find_one(
                dict(orgID=org_id, userName=user_name,
                     status=USER_STATUS_ACTIVATED))
        if not user:
            raise AuthorizationError(
                AuthorizationError.UserNameNotExists, msg='user not exist.')

        if self.get_argument('encrypt'):
            priv_key = await get_private_key_by_org_id(org_id)
            password = decrypt(password, priv_key).decode('utf8')
        check_password(user, password)

        jwt_data['uid'] = user.id
        jwt_data['uname'] = user.name
        jwt_data['avatar'] = user.avatar

        admin_role_id = await get_admin_role_id(org_id)
        if admin_role_id and admin_role_id in user.roleList:
            # 系统管理员
            jwt_data['super'] = 1
        else:
            super_role_id = await get_super_role_id()
            if super_role_id and super_role_id in user.roleList:
                # 超级管理员
                jwt_data['super'] = 1

        # 生成jwt
        token = jwt_utils.encode2str(**jwt_data)
        refresh_token = jwt_utils.encode2str(
            org_code=org_code,
            uid=user.id,
            timeout=settings.JWT_REFRESH_TIMEOUT)

        return SuccessData(token=token, refresh_token=refresh_token)


class AuthRefreshTokenHandler(BaseHandler):
    """
    刷新jwt
    """

    @decorators.render_json
    async def post(self):
        org_code = self.token_payload.get('org_code')
        user_id = self.token_payload.get('uid')

        jwt_data = {}

        if org_code:
            organization = await OrganizationDAO.find_one(dict(code=org_code, status=ORGANIZATION_STATUS_ACTIVATED))
            if not organization:
                raise AuthorizationError(
                    AuthorizationError.OrgNotExists, msg='organization be disabled.')
            if organization.expiryDT:
                expire = organization.expiryDT
                expire = date(year=expire.year,
                              month=expire.month, day=expire.day)
                if date.today() > expire:
                    raise AuthorizationError(
                        AuthorizationError.OrgExpire, msg=str(expire))
                jwt_data['org_exp'] = str(expire)
            org_id = organization.oid
            jwt_data['org_code'] = organization.code
            jwt_data['org_name'] = organization.name
            jwt_data['org_id'] = str(org_id)
        else:
            org_id = None

        user = await UserDAO.get_by_id(user_id)
        if not user:
            raise AuthorizationError(
                AuthorizationError.UserNameNotExists, msg='user be disabled.')

        if not user.orgID == org_id:
            raise AuthorizationError(
                AuthorizationError.PwdError, msg='user is inconsistent with the organization.')

        jwt_data['uid'] = user.id
        jwt_data['uname'] = user.name
        jwt_data['avatar'] = user.avatar

        admin_role_id = await get_admin_role_id(org_id)
        if admin_role_id in user.roleList:
            # 系统管理员
            jwt_data['super'] = 1
        else:
            super_role_id = await get_super_role_id()
            if super_role_id in user.roleList:
                # 超级管理员
                jwt_data['super'] = 1

        # 生成jwt
        token = jwt_utils.encode2str(**jwt_data)
        refresh_token = jwt_utils.encode2str(
            org_code=org_code,
            uid=user.id,
            timeout=settings.JWT_REFRESH_TIMEOUT)

        return SuccessData(token=token, refresh_token=refresh_token)


URL_MAPPING_LIST = [
    url(r'/api/authorize/token/', AuthTokenHandler, name='authorize_token'),
    url(r'/api/authorize/token/refresh/', AuthRefreshTokenHandler, name='authorize_token_refresh'),
]
