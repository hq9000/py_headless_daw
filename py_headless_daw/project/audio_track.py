from typing import List, Optional

from py_headless_daw.project.plugins.effect import Effect
from py_headless_daw.project.project import Track


class AudioTrack(Track):
    GAIN: str = 'gain'
    PANNING: str = 'panning'

    def __init__(self):
        super().__init__()
        self.effects: List[Effect] = []

        self.add_parameter(self.GAIN, 1.0)
        self.add_parameter(self.PANNING, 0.0)
