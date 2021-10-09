import os
from .memorizer_base import BaseMemorizer
from commons.Helpers.Helper_productor import Productor
from core import config


class MemorizerProductor(Productor):
    def __init__(self, root_dir, start_dir, base_module, temp_module, pattern="*.py") -> object:
        super().__init__(root_dir, start_dir, base_module, temp_module, pattern)


base_name = os.path.join(os.path.dirname(__file__))
memorizer_productor = MemorizerProductor(config.SITE_ROOT, base_name, BaseMemorizer, BaseMemorizer, "*.py")
