import os

from productor import Productor

import core

# 本模块方法
from .memorizer_base import BaseMemorizer

base_name = os.path.join(os.path.dirname(__file__))
memorizer_productor = Productor(core.path.SITE_ROOT, base_name, BaseMemorizer, BaseMemorizer)
