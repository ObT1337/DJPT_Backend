from flaskDj import dataio
from flaskDj.classes import TrackCollection
from flaskDj.manager import PlaylistManager, PlaylistTracksManager, TracksManager
from sqlalchemy import MetaData, Table, create_engine, inspect, text


class DatabaseService:
    def __init__(self, app):
        self.app = app
        self.db = self.app.db
        self.session = self.db.session
        self.db_ui: str = self.app.config["SQLALCHEMY_DATABASE_URI"]
        self.engine = create_engine(self.db_ui)
        self.pl_manager = PlaylistManager(app)
        self.plt_manager = PlaylistTracksManager(app)
        self.track_manager = TracksManager(app)

    def column_exists_in_table(self, table_name, column_name):
        inspector = inspect(self.engine)
        columns = [column["name"] for column in inspector.get_columns(table_name)]
        return column_name in columns

    def init_db(self):
        self.db.drop_all()
        self.db.create_all()
        return f"Initialized the database with the following tables: {list(self.get_all_tables())} ."

    def get_table(self, tablename: str):
        table = Table(tablename, self.db.metadata, autoload_with=self.engine)
        return table.select().execute().fetchall()

    def table_exists(self, name):
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        return name in metadata.tables

    def get_all_tables(self):
        metadata = self.db.MetaData()
        metadata.reflect(bind=self.engine)
        return metadata.tables.keys()

    def import_from_directory(self, directory: str) -> str:
        collection = TrackCollection(tracks=dataio.get_files_from_directory(directory))
        from flaskDj.models import Tracks

        tracks = [
            Tracks(
                title=i.title,
                artist=i.artist,
                album=i.album,
                duration=i.duration,
                bpm=i.bpm,
                genre=i.genre,
                openKey=i.open_key,
                musicalKey=i.musical_key,
                musicalKeySharps=i.musical_key_sharps,
                added=i.added,
                date=i.date,
                playCount=i.play_count,
                fileLocation=i.path,
            )
            for i in collection.tracks
        ]
        added, tracks = self.track_manager.add_Tracks(tracks)
        if added:
            return f"Added the following Tracks to the library:{tracks}."
        return "All tracks have already been added to the library."

    def add_tracks_to_playlist(self, playlist_name, *args, **kwargs):
        playlist = self.pl_manager.get_or_create_playlist(playlist_name)
        self.plt_manager.add_tracks_to_playlist(playlist, *args, **kwargs)

    def delete_tracks_from_playlist(self, playlist_name, *args, **kwargs):
        playlist = self.pl_manager.get_or_create_playlist(playlist_name)
        self.plt_manager.delete_tracks_from_playlist(playlist, *args, **kwargs)

    def move_track_to_position(self, playlist_name, *args, **kwargs):
        playlist = self.pl_manager.get_or_create_playlist(playlist_name)
        self.plt_manager.move_track(playlist, *args, **kwargs)

    def get_track(self, track_id):
        return self.track_manager.get_entry_from_id(track_id)
