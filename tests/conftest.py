import pytest
from django.conf import settings
from optics.settings.components import config

# https://pytest-django.readthedocs.io/en/latest/database.html#using-an-existing-external-database-for-tests
@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_DATABASE_NAME"),
        "USER": "root",
        "PASSWORD": config("DB_ROOT_PASSWORD"),
        "HOST": config("DJANGO_DATABASE_HOST"),
        "PORT": config("DJANGO_DATABASE_PORT", cast=int),
        "TEST": {
            "NAME": "Optics_Test_db",
        },
    }
