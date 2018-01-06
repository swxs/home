# -*- coding: utf-8 -*-
'''
@author: xuyi
@created: 2016-12-22 16:51:09
@description:
@updated: 2016-12-22 16:51:09
'''
import functools
import tornado
# import company.bil as company_bil
# import company.bil_relation as bil_relation
# from company import enum, utils
import const
from base import BaseHandler
# from api.organization.permission import utils as permission_utils
# from api.organization.region import utils as region_utils
# from common.exception import NotLoginException, PermException


def with_permission(*perm_list):
    '''判断用户是否有指定权限
    '''
    def _decorator(method):
        ''''''
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            ''''''
            # user = self.current_user
            # # user = utils.get_user('595f625c1d41c81b48f799e5')
            # if not user:
            #     raise NotLoginException()
            # for permission in perm_list:
            #     if not permission_utils.has_permission(user, permission):
            #         raise PermException()
            # else:
            #     return method(self, *args, **kwargs)
            return True
        return wrapper
    return _decorator


# def frontend_check_region():
#     '''判断用户数据可见范围
#     '''
#     def _decorator(method):
#         ''''''
#         @functools.wraps(method)
#         def wrapper(self, *args, **kwargs):
#             ''''''
#             user = self.current_user
#             if not user:
#                 raise NotLoginException()
#             temp_region_list = list(region_utils.get_region_by_admin_user(user.oid))
#             # user = utils.get_user('595f625c1d41c81b48f799e5')
#
#             for permission in perm_list:
#                 if not permission_bil.has_permission(user, permission):
#                     raise PermException()
#             else:
#                 return method(self, *args, **kwargs)
#         return wrapper
#     return _decorator
#
#
# def with_role(role):
#     ''''''
#     role = permission_bil(role)
#
#     def _decorator(method):
#         ''''''
#         @functools.wraps(method)
#         def wrapper(self, *args, **kwargs):
#             ''''''
#             user = self.current_user
#             if user and role.oid in user.role_list:
#                 method(self, *args, **kwargs)
#             else:
#                 self.set_status(404)
#         return wrapper
#     return _decorator
#
#
# def administrator_only(method):
#     ''''''
#     @functools.wraps(method)
#     def wrapper(self, *args, **kwargs):
#         ''''''
#         user = self.current_user
#         if not user or user.administrator != 1:
#             n = tornado.escape.url_escape(self.request.uri)
#             self.redirect(self.reverse_url('system_login') + '?next=' + n)
#         else:
#             method(self, *args, **kwargs)
#     return wrapper
#
#
# def admin_only(method):
#     ''''''
#     @functools.wraps(method)
#     def wrapper(self, *args, **kwargs):
#         ''''''
#         user = self.current_user
#         if not user or user.admin != 1:
#             n = tornado.escape.url_escape(self.request.uri)
#             self.redirect(self.reverse_url('login') + '?next=' + n)
#         else:
#             method(self, *args, **kwargs)
#     return wrapper
#
#
# def dealer_admin(method):
#     ''''''
#     @functools.wraps(method)
#     def wrapper(self, dealer_id, *args, **kwargs):
#         ''''''
#         user = self.current_user
#         if not user:
#             n = tornado.escape.url_escape(self.request.uri)
#             self.redirect(self.reverse_url('login') + '?next=' + n)
#         else:
#             dealer = company_bil.get_dealer(dealer_id)
#             if not dealer:
#                 self.set_status(404)
#                 return
#
#             du = bil_relation.get_du_by_dealer_user(dealer, self.current_user)
#             if not du or du.admin != const.yes_or_no['yes']:
#                 self.set_status(404)
#                 return
#
#             method(self, dealer, *args, **kwargs)
#     return wrapper
#
#
# def structure_admin(method):
#     ''''''
#     @functools.wraps(method)
#     def wrapper(self, structure_id, *args, **kwargs):
#         ''''''
#         user = self.current_user
#         if not user:
#             n = tornado.escape.url_escape(self.request.uri)
#             self.redirect(self.reverse_url('login') + '?next=' + n)
#         else:
#             structure = company_bil.get_structure(structure_id)
#             if not structure:
#                 self.set_status(404)
#                 return
#
#             su = bil_relation.get_su_by_structure_user(
#                 structure, self.current_user)
#             if not su or su.admin != const.yes_or_no['yes']:
#                 self.set_status(404)
#                 return
#
#             method(self, structure, *args, **kwargs)
#     return wrapper
