from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskDj import config, factory

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
migrate = Migrate(app, db)
app.db = db
app.migrate = Migrate

if __name__ == "__main__":
    app = factory.create_app(app, config_object=config.DevelopmentConfig)
