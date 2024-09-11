import os

from productor import Productor

import core

# 本模块方法
from .manager_base import BaseManager, BaseManagerQuerySet

base_name = os.path.join(os.path.dirname(__file__))
manager_productor = Productor(core.path.SITE_ROOT, base_name, BaseManager, BaseManager)
