import os
import locale
from flaskDj.blueprints import api,helloworld

class Config:
    SECRET_KEY = "dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANG="de_DE"
    locale.setlocale(locale.LC_ALL, LANG)
    BLUEPRINTS=[api,helloworld]


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.getcwd(), "instance", "flaskDj.sqlite"
    )
