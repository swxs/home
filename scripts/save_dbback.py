import os
import sys
import click
from commons.Helpers import mongodb_dumper_helper
from commons.Helpers.ApiHelper_Baidupan import PCS


def main():
    filepath = mongodb_dumper_helper.dump()

    path, dir_name = os.path.split(filepath)
    filename = f"{dir_name}.tar.gz"
    tar_filepath = os.path.join(path, filename)
    os.system(f"tar -czvf {tar_filepath} {filepath}")

    pan_helper = PCS("iamoom", "A1e35c6ee471")
    with open(tar_filepath, "rb") as f:
        pan_helper.upload("/dbback/", f, filename)


if __name__ == "__main__":
    main()
