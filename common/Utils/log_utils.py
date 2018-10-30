import logging
import logging.config
import os

script_path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(os.path.join(script_path, 'logging.conf'))
logging.getLogger('asyncio').setLevel(logging.WARNING)


def getLogger(name=None, console=False):
    BASE = "root" if console else "main"
    if name:
        logger = logging.getLogger(f"{BASE}.{name}")
    else:
        logger = logging.getLogger(BASE)
    return logger
