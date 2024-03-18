# -*- coding: utf-8 -*-
# @FILE    : models/user.py
# @AUTH    : code_creater

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from dao.managers.manager_sqlalchemy import Base, Ix


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME(fsp=6))
    updated = Column(DATETIME(fsp=6))
    username = Column(String(32))
    description = Column(Boolean, default=True)
    avatar = Column(Integer)

    __table_args__ = (Ix(keys=['username'], unique=True),)


class UserAuth(Base):
    __tablename__ = "userauth"

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME(fsp=6))
    updated = Column(DATETIME(fsp=6))
    user_id = Column(Integer)
    ttype = Column(Integer)
    identifier = Column(String(32))
    credential = Column(String(32))
    ifverified = Column(Integer)

    user = relationship(
        "User",
        primaryjoin='foreign(User.id) == UserAuth.user_id',
        lazy='selectin',
        backref=backref('user', lazy='joined'),
    )

    __table_args__ = (
        Ix(keys=['user_id']),
        Ix(keys=['ttype', 'identifier'], unique=True),
    )
