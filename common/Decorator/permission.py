import functools
from common.Exceptions import *


def Permission(*perm_list):
    '''
    判断用户是否有指定权限
    '''

    def _decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            pass

        return wrapper

    return _decorator

