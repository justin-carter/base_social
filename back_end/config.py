import os

from back_end.helpers.connection import get_postgres_url

# database
SQLALCHEMY_DATABASE_URI = get_postgres_url()
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQL_ECHO = os.getenv('SQL_ECHO', False)

# jwt secret key
SECRET_KEY = os.getenv('SECRET_KEY')
