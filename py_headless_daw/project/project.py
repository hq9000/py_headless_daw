from py_headless_daw.project.track import Track


class Project:
    def __init__(self, master_track: Track):
        self.master_track: Track = master_track
        self.num_audio_channels = 2
        pass
