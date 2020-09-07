from invoke import task

from barnacles.misha import AlembicCommand
from barnacles.store import Local


@task
def db_revision(context, message=None):
    AlembicCommand().autogenerate_revision(message=message)


@task
def db_upgrade(context):
    AlembicCommand().update_database()


@task
def show_barnacles(context):
    print(Local().path())
