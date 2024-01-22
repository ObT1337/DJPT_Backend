import os

from flask import Flask
from flaskDj import manager
from flaskDj.blueprints import main
from flaskDj.commands import init_commands


def create_app(app: Flask, config_object="config.DevelopmentConfig"):
    app.config.from_object(config_object)

    # Load instance config, if it exists
    app.config.from_pyfile("config.py", silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.db.init_app(app)
    app.table_man = manager.TableManger(app)
    app.tracks_man = manager.TracksManager(app)
    app.playlist_man = manager.PlaylistManager(app)

    with app.app_context():
        # Create database tables
        from flaskDj import models

        app.db.create_all()

        # Import and register blueprints

        app.register_blueprint(main.bp)

        # Import and run commands

        init_commands(app)

    return app
