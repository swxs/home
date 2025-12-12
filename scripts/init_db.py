from sqlalchemy import create_engine

from core import config
from mysqlengine import Base


def register_database():
    # 预先创建数据表
    from apps.password_lock.models import password_lock
    from apps.system.models import (
        oauth_authorization_code,
        oauth_client,
        user,
        user_auth,
    )
    from apps.upload.models import file_info
    from apps.wechat.models import wechat_msg

    if config.MYSQL_USERNAME and config.MYSQL_PASSWORD:
        MYSQL_URL = f"mariadb+pymysql://{config.MYSQL_USERNAME}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}?charset=utf8mb4"
    else:
        MYSQL_URL = f"mariadb+pymysql://{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}?charset=utf8mb4"

    sync_engine = create_engine(MYSQL_URL, pool_size=config.MYSQL_POOL_SIZE)

    Base.metadata.create_all(bind=sync_engine)


register_database()
