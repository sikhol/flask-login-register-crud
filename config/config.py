import os
import datetime
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DEBUG = os.getenv('DEBUG')
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_BLACKLIST_ENABLED = False
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refres']
    # JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=2)
    MAIL_SERVER =os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
