# -*- coding: utf-8 -*-
# @File    : manager_productor.py
# @AUTH    : swxs
# @Time    : 2019/10/4 19:59

import os
from document_utils.manager.manager_base import BaseManager
from common.Helpers.Helper_productor import Productor
import settings


class ManagerProductor(Productor):
    def __init__(self, root_dir, start_dir, base_module, temp_module, pattern="*.py") -> object:
        super().__init__(root_dir, start_dir, base_module, temp_module, pattern)


base_name = os.path.join(os.path.dirname(__file__), "manager")
manager_productor = ManagerProductor(settings.SITE_ROOT, base_name, BaseManager, BaseManager, "*.py")
