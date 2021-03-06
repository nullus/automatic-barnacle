from sqlalchemy import Column, Integer, String, Binary, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class TablePrefix(object):
    """Mixin to provide default table naming"""

    PREFIX = "barnacles_"

    @declared_attr
    def __tablename__(self):
        return self.PREFIX + self.__name__.lower()


class SurrogateKeyId(object):
    """Mixin to add an auto increment surrogate primary key (id)"""

    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True, nullable=False)


class Tag(Base, TablePrefix, SurrogateKeyId):
    tag = Column(String(50), nullable=False)


class VideoTags(Base, TablePrefix, SurrogateKeyId):
    tag_id = Column(Integer, index=True, nullable=False)
    video_id = Column(Integer, index=True, nullable=False)


class Video(Base, TablePrefix, SurrogateKeyId):
    uuid = Column(String(36), unique=True, nullable=False)
    path = Column(String(260), nullable=False)


class MediaItem(Base, TablePrefix, SurrogateKeyId):
    hash = Column(Binary(32), unique=True, nullable=False)
    path = Column(Text(), nullable=False)
