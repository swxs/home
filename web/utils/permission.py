import functools


@property
def access_token(self):
    if not hasattr(self, '_access_token'):
        self._access_token = self.request.headers.get('access_token').replace("Bearer ", "")
    return self._access_token


@access_token.setter
def access_token(self, token):
    self._headers.add('access_token', f"Bearer {token}")


@property
def refresh_token(self):
    if not hasattr(self, '_refresh_token'):
        self._refresh_token = self.request.headers.get('refresh_token').replace("Bearer ", "")
    return self._refresh_token


@refresh_token.setter
def refresh_token(self, token):
    self._headers.add('refresh_token', f"Bearer {token}")


def permission(*perm_list):
    """
    判断用户是否有指定权限
    """

    def _decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            pass

        return wrapper

    return _decorator
