import os
from .manager_base import BaseManager
from commons.Helpers.Helper_productor import Productor
from core import config


class ManagerProductor(Productor):
    def __init__(self, root_dir, start_dir, base_module, temp_module, pattern="*.py") -> object:
        super().__init__(root_dir, start_dir, base_module, temp_module, pattern)


base_name = os.path.join(os.path.dirname(__file__))
manager_productor = ManagerProductor(config.SITE_ROOT, base_name, BaseManager, BaseManager, "*.py")
