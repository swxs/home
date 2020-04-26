import asyncio
import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __repr__(self):
       return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                            self.name, self.fullname, self.nickname)

def run():
    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine("mysql://root:swxs@localhost/runoob",
                            encoding='latin1', echo=True)
    Base.metadata.create_all(engine)

    # ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

    Session = sessionmaker(bind=engine)
    session = Session()
    # session.add(ed_user)
    session.add_all([
        User(name='wendy', fullname='Wendy Williams', nickname='windy'),
        User(name='mary', fullname='Mary Contrary', nickname='mary'),
        User(name='fred', fullname='Fred Flintstone', nickname='freddy')
    ])
    session.commit()

    for row in session.query(User.name.label('name_label')).all():
        print(row.name_label)


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(run())
    # print(result)

    run()
