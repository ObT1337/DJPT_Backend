import glob
import os

from .classes import FileType
from .logger import Logger
from .settings import LoggerSettings

log = Logger("dataio", LoggerSettings.log_level)


# from .classes import TrackCollection
# def open_tracks(self, tracks: TrackCollection):
#     self.collection += tracks
#     self.focused_collection = tracks
#     self.load_track(0, tracks)


# def load_track(self, identifier, tracks: None | TrackCollection = None):
#     if tracks:
#         self.selected_tracks = tracks
#         if isinstance(identifier, str):
#             identifier, _ = self.selected_tracks.get_track_by_path(identifier)
#         self.re_init_track_table(tracks, identifier)
#     if isinstance(identifier, int):
#         track = self.collection[identifier]
#         index = identifier
#     else:
#         index, track = self.collection.get_track_by_path(identifier)


def get_files_from_directory(directory):
    if not directory:
        return

    all_files = glob.glob(os.path.join(directory, "**"), recursive=True)
    return [
        os.path.abspath(file)
        for file in all_files
        if os.path.isfile(file) and file.endswith(tuple(ft.value for ft in FileType))
    ]
