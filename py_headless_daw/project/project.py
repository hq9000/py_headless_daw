from typing import Optional

from py_headless_daw.project.track import Track


class Project:
    def __init__(self, master_track: Track):
        self.start_time_seconds: Optional[float] = None
        self.end_time_seconds: Optional[float] = None

        self.master_track: Track = master_track
        self.num_audio_channels = 2
        pass
