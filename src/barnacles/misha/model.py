from sqlalchemy import Column, Integer, Binary, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class WithDefaultTablename:
    """Mixin to provide default table naming"""

    PREFIX = "misha_"

    @declared_attr
    def __tablename__(self):
        return self.PREFIX + self.__name__.lower()


class WithSurrogateKeyId:
    """Mixin to add an auto increment surrogate primary key (id)"""

    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer(), primary_key=True, nullable=False)


class AddressPath(WithSurrogateKeyId, WithDefaultTablename, Base):
    hash = Column(Binary(32), unique=True, index=True, nullable=False)
    path = Column(Text(), nullable=False)
