#! python3
import configparser
import os

from flask.cli import FlaskGroup
from flaskDj import app
from flaskDj.config import DevelopmentConfig
from flaskDj.factory import create_app

# config = configparser.ConfigParser()
# INI_PATH = os.path.abspath(os.path.join("flaskDj", "config.ini"))
# DEFAULT_INI_PATH = os.path.abspath(os.path.join("flaskDj", "default_ini"))
# with open(DEFAULT_INI_PATH) as f:
#     config.read_file(f)
# config.read([INI_PATH, INI_PATH], encoding="cp1250")


cli = FlaskGroup(
    create_app=lambda *args, **kwargs: create_app(
        app, DevelopmentConfig(), *args, **kwargs
    )
)

if __name__ == "__main__":
    cli()
