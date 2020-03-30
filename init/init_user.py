import sys
import os
import yaml
import settings
from apps.consts.const import undefined
from apps.utils.user import User


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


def init_system():
    pass


def main():
    init_system()


if __name__ == "__main__":
    main()
