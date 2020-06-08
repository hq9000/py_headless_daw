from typing import List

from py_headless_daw.project.track import Track


class Project:
    def __init__(self):
        self.tracks: List[Track] = []
        pass

    def add_tracks(self, *tracks: Track):
        for track in tracks:
            track.project = self
            self.tracks.append(track)
