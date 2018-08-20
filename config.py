from os import environ

SECRET_KEY = environ.get("SECRET_KEY")
DATABASE_URI = environ.get("DATABASE_URI")
TEST_DATABASE_URI = environ.get("TEST_DATABASE_URI")
