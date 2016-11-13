from setuptools import setup, find_packages

setup(
    name = 'barnacles',
    version = '1.0.2',
    packages = find_packages(),
    requires = [
        "flask",
        "rarfile",
        "sqlalchemy",
        "alembic",
    ],
)
