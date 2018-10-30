import sys
import os

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))

import fire
import yaml
import settings
from api.consts.const import undefined
from api.utils.user import User

def init_user():
    with open(settings.INIT_SETTINGS_FILE, "rb") as file:
        user_list = yaml.load(file).get("user")

    for user in user_list:
        User.create(
            username=user.get('username', undefined),
            nickname=user.get('nickname', undefined),
            password=user.get('password', undefined),
            key=user.get('key', undefined)
        )


if __name__ == "__main__":
    fire.Fire(init_user)
    print("----------user初始化完成----------")