from setuptools import setup, find_packages

setup(
    name = 'barnacles',
    version = '1.1.1',
    packages = find_packages(),
    install_requires = [
        "flask",
        "rarfile",
        "sqlalchemy",
        "alembic",
    ],
    package_data = {
        '': ['templates/*.html'],
    },
    extras_require = {
        'test': 'waitress',
    }
)
