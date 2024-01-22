from flaskDj import db


class Tracks(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255))
    duration = db.Column(db.Time)
    bpm = db.Column(db.Integer)
    genre = db.Column(db.String(255))
    openKey = db.Column(db.String(255))
    musicalKey = db.Column(db.String(255))
    musicalKeySharps = db.Column(db.String(255))
    added = db.Column(db.DateTime, default=db.func.current_timestamp())
    date = db.Column(db.Date)
    playCount = db.Column(db.Integer, default=0)
    fileLocation = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return f"<Track {self.artist}-{self.title}>"


class Playlists(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    tracks = db.relationship("PlaylistTracks", backref="playlist", lazy=True)


class PlaylistTracks(db.Model):
    __tablename__ = "playlists_tracks"
    id = db.Column(db.Integer, primary_key=True)

    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=False)
    position = db.Column(db.Integer, nullable=False)
