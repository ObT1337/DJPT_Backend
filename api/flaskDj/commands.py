from flask import Flask, current_app
from flaskDj.logger import Logger
from flaskDj.manager import PlaylistManager, PlaylistTracksManager, TracksManager
from flaskDj.service import DatabaseService
from flaskDj.settings import LoggerSettings

log = Logger("Database", LoggerSettings.log_level)
import click
from flask.cli import with_appcontext


class DatabaseCommands:
    @with_appcontext
    def __init__(self) -> None:
        self.service = DatabaseService(current_app)

    @staticmethod
    @click.command("init-db")
    @with_appcontext
    def init_db():
        """Clear the existing data and create new tables."""
        service = DatabaseService(current_app)
        log.debug(service.init_db())

    @staticmethod
    @click.command("list-tables")
    @with_appcontext
    def list_all_tables():
        """Lists all data tables contained in the database."""
        service = DatabaseService(current_app)
        log.debug(service.get_all_tables())

    @staticmethod
    @click.command("show")
    @click.argument("name")
    @with_appcontext
    def get_table(name):
        service = DatabaseService(current_app)
        """Lists all data tables contained in the database."""
        log.debug(service.get_table(name))

    @staticmethod
    @click.command("import-dir")
    @click.argument("directory")
    @with_appcontext
    def import_from_directory(directory: str):
        """Import all files from directory."""
        service = DatabaseService(current_app)
        log.debug(service.import_from_directory(directory))


class PlaylistCommands:
    @with_appcontext
    def __init__(self) -> None:
        self.manager = PlaylistManager(current_app)

    @staticmethod
    @click.command("add-playlist")
    @click.argument("name")
    @click.option("--overwrite", is_flag=True)
    def add_playlist(name: str, overwrite: bool = False):
        """Add a new table to the database.

        Args:
            name (str): Name of the Table.
            overwrite (bool): If True a new table is created even so one already exists.
        """
        manager = PlaylistManager(current_app)
        log.debug(manager.create_playlist(name, overwrite))

    @staticmethod
    @click.command("delete-playlist")
    @click.argument("name")
    @with_appcontext
    def delete_playlist(name: str):
        """Delete a new table to the database.

        Args:
            name (str): Name of the Table
        """
        manager = PlaylistManager(current_app)
        log.debug(manager.delete_playlist(name))


class PlaylistTracksCommands:
    @staticmethod
    @click.command("add-to")
    @click.argument("playlist_name")
    @click.argument("track")
    @click.option("--duplicates", is_flag=True)
    @with_appcontext
    def add_track_to_playlist(playlist_name: str, track: int, duplicates: bool = False):
        """Import all files from directory."""
        service = DatabaseService(current_app)
        log.debug(
            service.add_tracks_to_playlist(playlist_name, track, duplicates=duplicates)
        )

    @staticmethod
    @click.command("delete-from")
    @click.argument("playlist")
    @click.argument("track")
    @with_appcontext
    def delete_track_from_playlist(playlist: str, track: int):
        """Import all files from directory."""
        service = DatabaseService(current_app)
        log.debug(service.delete_tracks_from_playlist(playlist, track))


class TracksCommands:
    @with_appcontext
    def __init__(self) -> None:
        self.manager = TracksManager(current_app)


def init_commands(app: Flask):
    commands = [
        DatabaseCommands.init_db,
        DatabaseCommands.get_table,
        DatabaseCommands.list_all_tables,
        DatabaseCommands.import_from_directory,
        PlaylistCommands.add_playlist,
        PlaylistCommands.delete_playlist,
        PlaylistTracksCommands.add_track_to_playlist,
        PlaylistTracksCommands.delete_track_from_playlist,
    ]
    for cmd in commands:
        app.cli.add_command(cmd)
