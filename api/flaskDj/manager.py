import os

import sqlalchemy
from flask import Flask
from flaskDj import dataio
from flaskDj.classes import TrackCollection
from flaskDj.logger import Logger
from sqlalchemy import MetaData, create_engine, func, inspect, select, text
from sqlalchemy.orm import Session

log = Logger("Manager")


class TableManger:
    def __init__(self, app: Flask):
        self.app = app
        self.db_ui: str = self.app.config["SQLALCHEMY_DATABASE_URI"]
        self.db = self.app.db
        self.session = self.db.session
        self.engine = create_engine(self.db_ui)
        self.__tablename__ = None
        self.model = None

    def get_entry_from_id(self, identifier):
        return self.session.get(self.model, identifier)

    def get_entry_from_object(self, obj):
        return self.session.get(self.model, obj)

    def column_exists(self, column_name):
        inspector = inspect(self.engine)
        columns = [
            column["name"] for column in inspector.get_columns(self.__tablename__)
        ]
        return column_name in columns

    def read_sql_template(self, filename: str):
        if not filename.endswith(".sql"):
            filename += ".sql"
        sql_file = os.path.join("static", "sql", filename)
        with self.app.open_resource(sql_file) as f:
            return str(f.read().decode("utf8"))

    def add(self, entry: object):
        self.session.add(entry)
        self.session.commit()

    def delete(self, entry):
        self.session.delete(entry)
        self.session.commit()

    def add_bulk(self, entries: list):
        self.session.add_all(entries)
        self.session.commit()

    def execute(self, query: str):
        data = self.session.execute(text(query))
        self.commit()
        return data

    def commit(self):
        self.session.commit()

    def add_column(self, column_name, dtype):
        self.execute(
            f"ALTER TABLE {self.__tablename__} ADD COLUMN {column_name} {dtype}"
        )


class PlaylistManager(TableManger):
    def __init__(self, app: Flask):
        from flaskDj.models import Playlists

        super().__init__(app)

        self.__tablename__ = Playlists.__tablename__
        self.model = Playlists

    def get_or_create_playlist(self, name):
        from flaskDj.models import Playlists

        playlist = self.get_playlist(name)
        if not playlist:
            self.create_playlist(name)
            return self.get_or_create_playlist(name)
        return playlist

    def get_playlist(self, name):
        from flaskDj.models import Playlists

        return Playlists.query.filter_by(name=name).first()

    # def get_entry_from_playlist_entry(self, playlist_name, track_id):
    #     return self.execute(
    #         f"SELECT id FROM playlists WHERE {playlist_name} = {track_id} "
    #     ).fetchall()

    def create_playlist(self, name, overwrite=False):
        from flaskDj.models import Playlists

        pl_ex = self.playlist_exists(name)
        if overwrite:
            self.delete_playlist(name)
        else:
            if pl_ex:
                return f"Playlist {name} already exists in the database."

        self.add(Playlists(name=name))
        return f"Added playlist {name} to the database."

    def delete_playlist(self, name) -> str:
        pl_ex = self.playlist_exists(name)
        if not pl_ex:
            return f"Playlist {name} does not exists in the database."
        playlist = self.get_playlist(name)
        print(playlist.id)
        self.delete(playlist)
        return f"Deleted playlist {name} to the database."

    def playlist_exists(self, name):
        if self.get_playlist(name):
            return True
        return False


class PlaylistTracksManager(TableManger):
    def __init__(self, app: Flask):
        from flaskDj.models import PlaylistTracks

        super().__init__(app)

        self.__tablename__ = PlaylistTracks.__tablename__
        self.model = PlaylistTracks

    def add_tracks_to_playlist(
        self, playlist, track_ids, duplicates=False, position=None
    ):
        from flaskDj.models import PlaylistTracks

        if not isinstance(track_ids, list):
            track_ids = [track_ids]
        # If no position is provided, set it to the next available position
        tracks = []
        for tid in track_ids:
            if not duplicates and self.is_in_playlist(playlist.id, tid):
                continue

            if position is None:
                position = self.get_next_track_position(playlist)

            # Create a new PlaylistTracks entry
            tracks.append(
                PlaylistTracks(playlist_id=playlist.id, track_id=tid, position=position)
            )

        # Add to session and commit
        self.add_bulk(tracks)

    def get_next_track_position(self, playlist):
        from flaskDj.models import PlaylistTracks

        # Query the maximum position for the given playlist
        max_position = (
            self.session.query(func.max(PlaylistTracks.position))
            .filter_by(playlist_id=playlist.id)
            .scalar()
        )

        # If there are no tracks in the playlist yet, set position to 1
        if max_position is None:
            return 1

        # Otherwise, return the next available position
        return max_position + 1

    def move_track(self, playlist, current_entry, new_position):
        from flaskDj.models import PlaylistTracks

        # Get all that are above
        q = self.session.query(PlaylistTracks)(
            PlaylistTracks.playlist_id == playlist.id,
            PlaylistTracks.position > current_entry.position,
        )
        above = self.session.query(q).all()
        print(above)
        # Get all that are beneath
        q = self.session.query(PlaylistTracks)(
            PlaylistTracks.playlist_id == playlist.id,
            PlaylistTracks.position < current_entry.position,
        )
        beneath = self.session.query(q).all()
        print(beneath)

    def delete_tracks_from_playlist(self, playlist, track_ids):
        for tid in track_ids:
            track = self.get_track_entry(playlist.id, tid)
            self.delete(track)

    def get_track_entry(self, pl_id, track_id):
        from flaskDj.models import PlaylistTracks

        return PlaylistTracks.query.filter_by(
            playlist_id=pl_id, track_id=track_id
        ).first()

    def is_in_playlist(self, pl_id, track_id):
        if self.get_track_entry(pl_id, track_id):
            return True
        return False


class TracksManager(TableManger):
    def __init__(self, app: Flask):
        from flaskDj.models import Tracks

        super().__init__(app)

        self.__tablename__ = Tracks.__tablename__
        self.model = Tracks

    def add_Tracks(self, tracks):
        tracks = [track for track in tracks if not self.track_exist(track)]
        if len(tracks) != 0:
            self.add_bulk(tracks)
            return True, tracks
        return False, None

    def track_exist(self, track):
        with Session(self.engine) as session:
            # query for ``User`` objects
            statement = select(self.model).filter_by(fileLocation=track.fileLocation)

            # list of User objects
            obj = session.scalars(statement).all()
        return len(obj) != 0
