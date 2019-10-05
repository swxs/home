# -*- coding: utf-8 -*-
# @File    : manager_productor.py
# @AUTH    : swxs
# @Time    : 2019/10/4 19:59

import os
from document_utils.manager.manager_base import BaseManager
from common.Helpers.Helper_productor import Productor
import settings

base_name = os.path.join(os.path.dirname(__file__), "manager")


class ManagerProductor(Productor):
    def __init__(self, base_module: object, start_dir: object, pattern: object = '*.py', top_level_dir: object = None, temp_module: object = None) -> object:
        super().__init__(base_module, start_dir, pattern=pattern, top_level_dir=top_level_dir, temp_module=temp_module)
        self.root_dir = settings.SITE_ROOT


manager_productor = ManagerProductor(BaseManager, base_name, "*.py")
