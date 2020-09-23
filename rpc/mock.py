from mock import MagicMock
from rpc.main import gen_dispatcher
import settings


async def user_has_permission(*args, **kwargs):
    result = MagicMock()
    result.code = 0
    return result


class MockClient:
    def __init__(self):
        Dispatcher, _ = gen_dispatcher(settings.RPC_MODULE_LIST)
        self._oprot = MagicMock()
        self._oprot.trans.is_open.return_value = True
        self._dispatch = Dispatcher()
        self._dispatch.user_has_permission = user_has_permission
        self._dispatch.close = lambda: None

    def __getattr__(self, key):
        return getattr(self._dispatch, key)
