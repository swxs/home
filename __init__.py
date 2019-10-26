import asyncio
import datetime
import sys
from bson import ObjectId
from umongo import Instance, Document, fields, ValidationError, set_gettext
from umongo.marshmallow_bonus import SchemaFromUmongo
from pymongo import ASCENDING, DESCENDING
from motor.motor_asyncio import AsyncIOMotorClient

db = AsyncIOMotorClient()['home']
instance = Instance(db)


@instance.register
class BaseModelDocument(Document):
    created = fields.DateTimeField(default=datetime.datetime.now)
    updated = fields.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True
        allow_inheritance = True


@instance.register
class PasswordLock(BaseModelDocument):
    name = fields.StringField()
    key = fields.StringField()
    website = fields.StringField()
    user_id = fields.ObjectIdField()


@instance.register
class User(Document):
    nick = fields.StrField(required=True, unique=True)
    firstname = fields.StrField()
    lastname = fields.StrField()
    birthday = fields.DateTimeField()
    password = fields.StrField()  # Don't store it in clear in real life !


async def run():
    await User.collection.drop()
    await User.ensure_indexes()
    for data in [
        {
            'nick': 'mze', 'lastname': 'Mao', 'firstname': 'Zedong',
            'birthday': datetime.datetime(1893, 12, 26),
            'password': 'Serve the people'
        },
        {
            'nick': 'lsh', 'lastname': 'Liu', 'firstname': 'Shaoqi',
            'birthday': datetime.datetime(1898, 11, 24),
            'password': 'Dare to think, dare to act'
        },
        {
            'nick': 'lxia', 'lastname': 'Li', 'firstname': 'Xiannian',
            'birthday': datetime.datetime(1909, 6, 23),
            'password': 'To rebel is justified'
        },
        {
            'nick': 'ysh', 'lastname': 'Yang', 'firstname': 'Shangkun',
            'birthday': datetime.datetime(1907, 7, 5),
            'password': 'Smash the gang of four'
        },
        {
            'nick': 'jze', 'lastname': 'Jiang', 'firstname': 'Zemin',
            'birthday': datetime.datetime(1926, 8, 17),
            'password': 'Seek truth from facts'
        },
        {
            'nick': 'huji', 'lastname': 'Hu', 'firstname': 'Jintao',
            'birthday': datetime.datetime(1942, 12, 21),
            'password': 'It is good to have just 1 child'
        },
        {
            'nick': 'xiji', 'lastname': 'Xi', 'firstname': 'Jinping',
            'birthday': datetime.datetime(1953, 6, 15),
            'password': 'Achieve the 4 modernisations'
        }
    ]:
        await User(**data).commit()

    page = 1
    per_page = 10
    print(await User.count_documents())
    cursor = User.find(limit=per_page, skip=(page - 1) * per_page).sort([("nick", 1)])
    print([a.nick for a in await cursor.to_list(None)])

    cursor = User.find(limit=per_page, skip=(page - 1) * per_page)
    return [a.nick for a in await cursor.to_list(None)]
    cursor = User.find(limit=per_page, skip=(page - 1) * per_page).sort([("birthday", DESCENDING), ("nick", ASCENDING)])
    return len(await cursor.to_list(None))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(run()))
