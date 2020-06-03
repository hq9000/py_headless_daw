from typing import Optional, List

from py_headless_daw.project.plugins.effect import Effect
from py_headless_daw.project.plugins.synth import Synth


class Track:
    def __init__(self):
        self._synth: Optional[Synth] = None
        self._effects: List[Effect] = []
        self._gain: float = 1.0
        self._panning: float = 0.0




