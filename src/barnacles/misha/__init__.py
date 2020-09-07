from alembic.config import Config
from alembic import command

from barnacles.store import Local


class LocalStorage:

    def __init__(self, local: Local) -> None:
        super().__init__()
        self.local = local

    def db_url(self) -> str:
        path = self.local.path(["misha.sqlite"])
        #
        return f"sqlite:///{path}"

class AlembicConfig:
    def __init__(self, storage):
        self._config = Config()
        self._config.set_main_option('script_location', 'barnacles.misha:alembic')
        self._config.set_main_option('sqlalchemy.url', 'sqlite:///foobar.sqlite')

    @property
    def config(self):
        return self._config


class AlembicCommand(AlembicConfig):
    def autogenerate_revision(self, message=None):
        command.revision(self.config, message, autogenerate=True)

    def update_database(self):
        command.upgrade(self.config, revision="head")
