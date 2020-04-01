import sys
import os
import yaml
import asyncio
import settings
from apps.consts.const import undefined
from apps.System.utils.Organization import Organization
from apps.System.utils.User import User


async def init_system():
    with open(settings.INIT_SETTINGS_FILE, "rb") as file:
        organization_list = yaml.load(file).get("organization")
        user_list = yaml.load(file).get("user")

    org_dict = {}
    for organization in organization_list:
        org = await Organization.create(
            code=organization.get("code", undefined),
            name=organization.get("name", undefined),
            phone=organization.get("phone", undefined),
        )
        org_dict[organization.get("code", undefined)] = org.oid


    for user in user_list:
        User.create(
            org_id=org_dict.get(user.get('org_id').get('value', undefined), undefined),
            username=user.get('username', undefined),
            nickname=user.get('nickname', undefined),
            password=user.get('password', undefined),
            key=user.get('key', undefined)
        )


async def main():
    await init_system()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
