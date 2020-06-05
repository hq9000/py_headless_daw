from py_headless_daw.project.track import Track


class MidiTrack(Track):
    def __init__(self, channel: int):
        super().__init__()
        self.channel = channel
