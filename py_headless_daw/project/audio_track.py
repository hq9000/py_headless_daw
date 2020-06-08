from typing import List

from py_headless_daw.project.plugins.plugin import Plugin
from py_headless_daw.project.project import Track


class AudioTrack(Track):
    GAIN: str = 'gain'
    PANNING: str = 'panning'

    def __init__(self):
        super().__init__()
        self.add_parameter(self.GAIN, 1.0)
        self.add_parameter(self.PANNING, 0.0)
        self._plugins: List[Plugin] = []

    @property
    def plugins(self) -> List[Plugin]:
        return self._plugins

    @plugins.setter
    def plugins(self, plugins: List[Plugin]):
        self._plugins = plugins
