import glob
import hashlib
import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from . import dataio
from .classes import TrackCollection
from .logger import Logger
from .settings import LoggerSettings

log = Logger("Database", LoggerSettings.log_level)


class DatabaseService:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.connection = self.connect()

    @property
    def connection(self):
        return self.connect()

    @connection.setter
    def connection(self, value):
        self._connection = value

    def connect(self):
        connection = sqlite3.connect(self.db_uri, detect_types=sqlite3.PARSE_DECLTYPES)
        connection.row_factory = sqlite3.Row
        return connection

    def close_db(self, e=None):
        connection = g.pop("db", None)

        if connection is not None:
            connection.close()

    def init_db(self):
        sql_string = self.read_sql_template("schema.sql")
        self.execute(sql_string)
        return "Initialized the database."

    def get_all_tables(self):
        return self.execute(
            " SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

    def get_table(self, tablename: str):
        data = self.execute(f"SELECT * FROM {tablename}").fetchall()
        return "\n".join(data)

    def exists(self, name):
        data = self.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'; "
        ).fetchall()
        return data != []

    def add_entries(self, collection: TrackCollection, tablename: str):
        tracks = [
            (
                None,
                i.title,
                i.artist,
                i.album,
                str(i.duration),
                i.bpm,
                i.genre,
                i.open_key,
                i.musical_key,
                i.musical_key_sharps,
                i.added,
                i.date,
                i.play_count,
                i.path,
            )
            for i in collection.tracks
        ]
        sql_statement = (
            """INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
        )
        self.connection.cursor().executemany(sql_statement, tracks)
        self.connection.commit()
        return f"Added the following Tracks to the table {tablename}:{list(tracks)}"

    def import_from_directory(self, directory: str, tablename: str = "tracks") -> str:
        collection = TrackCollection(tracks=dataio.get_files_from_directory(directory))
        return self.add_entries(collection, tablename)

    def add_playlist(self, name, overwrite=False):
        sql_string = self.read_sql_template("schema.sql")
        if overwrite:
            self.delete_playlist(name)
        else:
            if self.exists(name):
                return f"Playlist {name} already exists in the the database."
        self.execute(sql_string.replace("tracks", name))
        return f"Added playlist {name} to the database."

    def delete_playlist(self, name) -> str:
        self.execute(f"DROP TABLE IF EXISTS {name};")
        return f"Deleted playlist {name} to the database."

    def read_sql_template(self, filename: str):
        sql_file = os.path.join("static", "sql", filename)
        with current_app.open_resource(sql_file) as f:
            return f.read().decode("utf8")

    def execute(self, query: str):
        return self.connection.executescript(query)

    @staticmethod
    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        """Clear the existing data and create new tables."""
        log.debug(DatabaseService(current_app.config["DATABASE"]).init_db())

    @staticmethod
    @click.command("add-playlist")
    @click.argument("name")
    @click.option("--overwrite", is_flag=True)
    @with_appcontext
    def init_add_playlist_command(name: str, overwrite: bool = False):
        """Add a new table to the database.

        Args:
            name (str): Name of the Table.
            overwrite (bool): If True a new table is created even so one already exists.
        """
        log.debug(
            DatabaseService(current_app.config["DATABASE"]).add_playlist(
                name, overwrite
            )
        )

    @staticmethod
    @click.command("delete-playlist")
    @click.argument("name")
    @with_appcontext
    def init_delete_playlist_command(name: str):
        """Delete a new table to the database.

        Args:
            name (str): Name of the Table
        """
        log.debug(DatabaseService(current_app.config["DATABASE"]).delete_playlist(name))

    @staticmethod
    @click.command("list-tables")
    @with_appcontext
    def init_list_all_tables_command():
        """Lists all data tables contained in the database."""
        log.debug(DatabaseService(current_app.config["DATABASE"]).get_all_tables())

    @staticmethod
    @click.command("show")
    @click.argument("tablename")
    @with_appcontext
    def init_get_table_command(tablename):
        """Lists all data tables contained in the database."""
        log.debug(DatabaseService(current_app.config["DATABASE"]).get_table(tablename))

    @staticmethod
    @click.command("import-dir")
    @click.argument("directory")
    @with_appcontext
    def init_import_from_directory_command(directory: str):
        """Import all files from directory."""
        log.debug(
            DatabaseService(current_app.config["DATABASE"]).import_from_directory(
                directory
            )
        )


def init_app(app):
    db = DatabaseService(app.config["DATABASE"])
    if not hasattr(app, "extensions"):
        app.extensions = {}
        app.extensions["db"] = db
    app.teardown_appcontext(db.close_db)

    commands = [
        db.init_db_command,
        db.init_add_playlist_command,
        db.init_delete_playlist_command,
        db.init_list_all_tables_command,
        db.init_import_from_directory_command,
        db.init_get_table_command
        # db.import_from_directory_command,
        # db.import_from_file_command,
    ]
    for cmd in commands:
        app.cli.add_command(cmd)
