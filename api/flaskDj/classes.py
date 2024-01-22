import os
import xml.etree.ElementTree as ET
from datetime import date, datetime, time, timedelta
from enum import Enum

from flaskDj.util import is_valid_date
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class FileType(Enum):
    mp3 = ".mp3"
    wav = ".wav"
    acc = ".acc"
    ogg = ".ogg"
    flac = ".flac"
    alac = ".alac"
    aiff = ".aiff"


class AudioTrack(EasyID3):
    def __init__(self, path: str):
        super().__init__(path)
        self.path: str = path
        self.ft: FileType = None
        self.title: str = None
        self.artist: str = None
        self.album: str = None
        self.date: date = None
        self.genre: str = None
        self.bpm: int = None
        self.play_count: int = 0
        self.full_name: str = None
        self.open_key: str = None
        self.musical_key: str = None
        self.musical_key_sharps: str = None
        self.added: date = None
        self.ft = self.identify_filetype()
        for key in ["title", "artist", "album", "date", "genre", "bpm"]:
            val = self.get(key)
            if val:
                self.__dict__[key] = f"{','.join(val)}"
        self.full_name = f"{self.artist} - {self.title}"
        self.date = self.init_date()
        self.duration = self.init_duration()

    def init_date(self) -> date:
        if self.date is not None:
            is_valid = is_valid_date(self.date)
            if is_valid:
                return is_valid

            if str(self.date).isdigit():
                return date(int(self.date), 1, 1)

        return None

    def init_duration(self) -> time:
        track = self.open_file()
        value = timedelta(seconds=track.info.length)

        # Convert timedelta to seconds
        total_seconds = int(value.total_seconds())

        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Create a datetime object with a fixed date and time
        dt = datetime(1900, 1, 1, hours, minutes, seconds)

        # Extract time component
        duration_time = dt.time()
        return duration_time

    @property
    def duration(self):
        return self.init_duration()

    @duration.setter
    def duration(self, value):
        self._duration = value

    def open_mp3(self):
        return MP3(self.path)

    def open_file(self):
        load_track = {FileType.mp3: self.open_mp3}
        if not self.ft:
            self.identify_filetype()
        return load_track[self.ft]()

    def identify_filetype(self):
        ft_ending = f".{os.path.basename(self.path).split('.')[-1]}"
        for ft in FileType:
            if ft_ending == ft.value:
                return ft

    def get_all_values(self):
        return [
            self.path,
            self.title,
            self.artist,
            self.album,
            self.date,
            self.genre,
            self.bpm,
        ]

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "duration": self.duration,
            "genre": self.genre,
            "openKey": self.open_key,
            "musicalKey": self.musical_key,
            "musicalKeySharps": self.musical_key_sharps,
            "added": self.added,
            "date": self.date,
            "filelocation": self.path,
            "album": self.album,
            "bpm": self.bpm,
        }

    def translate_to_apple_music(self):
        res = {}
        for key, value in self.to_dict().items():
            if key == "path":
                key = "Location"
                # value = value.replace(" ", "%20")
                value = f"file://{value}"
                # print(value)
            elif key == "title":
                key = "Name"
            elif key == "artist":
                key = "Artist"
            elif key == "album":
                key = "Album"
            elif key == "date":
                key = "Year"
            elif key == "genre":
                key = "Genre"
            elif key == "bpm":
                key = "BPM"
            res[key] = value
        return res


class TrackCollection:
    def __init__(self, tracks: list[AudioTrack]):
        self.name: str = None
        self.parent: str = None
        self.by_path: dict[str:AudioTrack] = {}
        self.by_title: dict[str : list[AudioTrack]] = {}
        self.by_artist: dict[str : list[AudioTrack]] = {}
        self.by_album: dict[str : list[AudioTrack]] = {}
        self.by_date: dict[str : list[AudioTrack]] = {}
        self.by_genre: dict[str : list[AudioTrack]] = {}
        self.by_bpm: dict[int : list[AudioTrack]] = {}
        self.playlists: dict = None
        if not self.parent:
            self.playlists: dict[TrackCollection] = {}
        self.init_tracks(tracks)

    def init_tracks(self, tracks: list[str]):
        """Initializes the List of Tracks."""
        audio_tracks = []
        for track in tracks:
            if isinstance(track, str):
                track = AudioTrack(path=track)
            elif not isinstance(track, AudioTrack):
                raise TypeError(
                    "Tracks in the attribute 'tracks' have to be of type AudioTrack or str"
                )
            audio_tracks.append(track)
        self.tracks = audio_tracks

    def __len__(self):
        return len(self.tracks)

    def __getitem__(self, index):
        return self.tracks[index]

    def __str__(self) -> str:
        return "\n".join([track.full_name for track in self.tracks])

    def __add__(self, other):
        for track in other.tracks:
            if track not in self.tracks:
                self.add_track(track)
        return self

    def to_list(self, dtype=None):
        if dtype == dict:
            return [track.to_dict() for track in self.tracks]

    def add_playlist(self, other):
        self.playlists[other.name] = other
        self += other

    def export_to_apple_music(self, filename):
        # Create the root element of the XML document
        root = ET.Element("plist")
        root.set("version", "1.0")
        root_dict = ET.SubElement(root, "dict")

        tracks_element = ET.SubElement(root_dict, "key")
        tracks_element.text = "Tracks"
        tracks_dict = ET.SubElement(root_dict, "dict")

        # Add each track to the track array as a dict
        for i, track in enumerate(self.tracks):
            track_id = ET.SubElement(tracks_dict, "key")
            track_id.text = str(i)

            track_dict = ET.SubElement(tracks_dict, "dict")
            track: AudioTrack
            a_track = track.translate_to_apple_music()
            a_track["Track ID"] = str(i)
            for key, value in a_track.items():
                if value is None or value == "":
                    continue
                key_element = ET.SubElement(track_dict, "key")
                key_element.text = key
                value: str
                if value.isnumeric():
                    value_element = ET.SubElement(track_dict, "integer")
                else:
                    value_element = ET.SubElement(track_dict, "string")
                value_element.text = value

        # Write the XML document to a file
        tree = ET.ElementTree(root)
        tree.write(filename, xml_declaration=True, encoding="utf-8")

    def add_track(self, track: AudioTrack):
        if track.path in self.by_path:
            return
        self.by_path[track.path] = track
        self.tracks.append(track)
        for i, data in enumerate(
            zip(
                [*track.get_all_values()],
                [
                    1,
                    self.by_title,
                    self.by_artist,
                    self.by_album,
                    self.by_date,
                    self.by_genre,
                    self.by_bpm,
                ],
            ),
        ):
            if i == 0:
                continue
            key, _dict = data
            if key not in _dict:
                _dict[key] = []
            _dict[key].append(track)

    def remove_track(self, track):
        if track.path not in self.by_path:
            return
        if track not in self.tracks:
            return
        self.tracks.remove(track)
        for key, _dict in zip(
            [*track.get_all_values()],
            [
                [],
                self.by_title,
                self.by_artist,
                self.by_album,
                self.by_date,
                self.by_genre,
                self.by_bpm,
            ],
        ):
            if track in dict[key]:
                _dict[key].remove(track)

    def init_dicts(self):
        for track in self.tracks:
            if track.path not in self.by_path:
                self.by_path[track.path] = track
            if track.title not in self.by_title:
                self.by_title[track.title] = []
            if track.artist not in self.by_album:
                self.by_artist[track.artist] = []
            if track.album not in self.by_album:
                self.by_album[track.album] = []
            if track.date not in self.by_date:
                self.by_date[track.date] = []
            if track.genre not in self.by_genre:
                self.by_genre[track.genre] = []
            if track.bpm not in self.by_bpm:
                self.by_bpm[track.bpm] = []
            for key, _dict in zip(
                [*track.get_all_values()],
                [
                    [],
                    self.by_title,
                    self.by_artist,
                    self.by_album,
                    self.by_date,
                    self.by_genre,
                    self.by_bpm,
                ],
            ):
                _dict[key].append(track)

    def get_track_by_path(self, path: str) -> tuple[int, AudioTrack]:
        track = self.by_path[path]
        i = self.tracks.index(track)
        return i, track

    def get_tracks_by_title(self, title: str) -> list[AudioTrack]:
        return self.by_title[title]

    def get_tracks_by_artist(self, artist: str) -> list[AudioTrack]:
        return self.by_artist[artist]

    def get_tracks_by_album(self, album: str) -> list[AudioTrack]:
        return self.by_album[album]

    def get_tracks_by_date(self, date: str) -> list[AudioTrack]:
        return self.by_date[date]

    def get_tracks_by_genre(self, genre: str) -> list[AudioTrack]:
        return self.by_genre[genre]

    def get_tracks_by_bpm(self, bpm: int) -> list[AudioTrack]:
        return self.by_bpm[bpm]

    def add_tracks_form_paths_list(self, paths: list[str]) -> None:
        for path in paths:
            self.add_track(AudioTrack(path))
