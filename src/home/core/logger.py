import logging
import logging.config
import os

from home.core.path import SITE_ROOT

logging.config.fileConfig(os.path.join(SITE_ROOT, "logging.ini"))
