from sqlalchemy import create_engine

from core import config
from mysqlengine import Base


def register_database():
    # 预先创建数据表
    from apps.password_lock.models import password_lock
    from apps.system.models import user, user_auth
    from apps.upload.models import file_info
    from apps.wechat.models import wechat_msg

    sync_engine = create_engine(
        "mysql+pymysql://swxs:C3f0a217f50e@localhost:3306/home?charset=utf8mb4",
        pool_size=config.MYSQL_POOL_SIZE,
    )

    Base.metadata.create_all(bind=sync_engine)


register_database()
