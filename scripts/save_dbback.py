import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.curdir))

import settings
from common.Helpers.Helper_mongodb import Helper_mongodb
from common.Helpers.ApiHelper_Baidupan import PCS

mongodb_backup_helper = Helper_mongodb()
filename = mongodb_backup_helper.dump()

pan_helper = PCS("iamoom", "A1e35c6ee471")
with open(os.path.join(settings.STATIC_DBBACK_PATH, filename), "rb") as f:
    pan_helper.upload("/dbback/", f, filename)
