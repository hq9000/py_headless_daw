from typing import Optional, List

from py_headless_daw.project.having_parameters import HavingParameters
from py_headless_daw.project.plugins.effect import Effect
from py_headless_daw.project.plugins.synth import Synth


class Track(HavingParameters):
    GAIN: str = 'gain'
    PANNING: str = 'panning'
    SEND1_GAIN: str = 'send1_gain'
    SEND1_PANNING: str = 'send1_panning'
    SEND2_GAIN: str = 'send2_gain'
    SEND2_PANNING: str = 'send2_panning'

    def __init__(self):
        super().__init__()
        self._synth: Optional[Synth] = None
        self._effects: List[Effect] = []

        self.add_parameter(self.GAIN, 1.0)
        self.add_parameter(self.PANNING, 0.0)

        self.add_parameter(self.SEND1_GAIN, 0.1)
        self.add_parameter(self.SEND1_PANNING, 0.0)

        self.add_parameter(self.SEND2_GAIN, 0.1)
        self.add_parameter(self.SEND2_PANNING, 0.0)
