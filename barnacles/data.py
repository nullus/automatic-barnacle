
import os
import sys

from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

def get_files():
    return [
        "/".join(os.path.relpath(os.path.join(walk[0], i), os.getcwd()).split(os.sep)).decode(sys.getfilesystemencoding())
        for walk in os.walk(os.getcwd())
        for i in walk[2]
        if i.lower().endswith('.mp4') or i.lower().endswith('.m4v')
    ]

class DefaultName(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class SurrogateKeyId(object):

    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True)


class Potato(Base, DefaultName, SurrogateKeyId):
    pass


class FileEntity(Base, DefaultName, SurrogateKeyId):

    api_id = Column(String(36), unique=True)
