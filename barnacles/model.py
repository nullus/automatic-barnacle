from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

class TablePrefix(object):
    PREFIX = "barnacles_"

    @declared_attr
    def __tablename__(cls):
        return cls.PREFIX + cls.__name__.lower()

class SurrogateKeyId(object):
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)


class Tag(Base, TablePrefix, SurrogateKeyId):
    tag = Column(String(50))

class Video(Base, TablePrefix, SurrogateKeyId):
    uuid = Column(String(36), unique=True)

