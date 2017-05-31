from os import environ

DEBUG = False
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
SECRET_KEY = environ.get('SECRET_KEY')
