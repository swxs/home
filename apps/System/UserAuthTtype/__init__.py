import os
import settings
from common.Helpers.Helper_productor import Productor
from .UserAuthTtypeBase import BaseTtypeUserAuth


class UserAuthTtypeProductor(Productor):
    def __init__(
        self,
        root_dir: object,
        start_dir: object,
        base_module: object = None,
        temp_module: object = None,
        pattern: object = '*.py'
    ):
        super().__init__(root_dir, start_dir, base_module=base_module, temp_module=temp_module, pattern=pattern)


base_path = os.path.join(settings.SITE_ROOT)
deliver_productor = UserAuthTtypeProductor(settings.SITE_ROOT, base_path, BaseTtypeUserAuth, BaseTtypeUserAuth, "*.py")
