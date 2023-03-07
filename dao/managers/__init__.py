import os

import core

# 通用方法
from commons.Helpers.Helper_productor import Productor

# 本模块方法
from .manager_base import BaseManager, BaseManagerQuerySet


class ManagerProductor(Productor):
    def __init__(self, root_dir, start_dir, base_module, temp_module, pattern="*.py") -> object:
        super().__init__(root_dir, start_dir, base_module, temp_module, pattern)


base_name = os.path.join(os.path.dirname(__file__))
manager_productor = ManagerProductor(core.path.SITE_ROOT, base_name, BaseManager, BaseManager, "*.py")
