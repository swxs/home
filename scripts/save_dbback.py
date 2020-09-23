import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.curdir))

import settings
from commons.Helpers.Helper_mongodb import Helper_mongodb
from commons.Helpers.ApiHelper_Baidupan import PCS

mongodb_backup_helper = Helper_mongodb()
filepath = mongodb_backup_helper.dump()

path, dir_name = os.path.split(filepath)
filename = f"{dir_name}.tar.gz"
tar_filepath = os.path.join(path, filename)
os.system(f"tar -czvf {tar_filepath} {filepath}")

pan_helper = PCS("iamoom", "A1e35c6ee471")
with open(tar_filepath, "rb") as f:
    pan_helper.upload("/dbback/", f, filename)
