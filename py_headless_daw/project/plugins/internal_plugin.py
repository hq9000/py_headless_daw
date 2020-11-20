from typing import List

from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.parameter import Parameter
from py_headless_daw.project.plugins.plugin import Plugin


class InternalPlugin(Plugin):
    pass


class GainPlugin(InternalPlugin):
    PARAMETER_GAIN: str = 'gain'

    def __init__(self):
        super().__init__()
        self.add_parameter(self.PARAMETER_GAIN, 1.0, Parameter.TYPE_FLOAT, (0, 1.0))


class PanningPlugin(InternalPlugin):
    PARAMETER_PANNING: str = 'panning'

    def __init__(self):
        super().__init__()
        self.add_parameter(self.PARAMETER_PANNING, 0.0, Parameter.TYPE_FLOAT, (-1.0, 1.0))


class SamplerPlugin(InternalPlugin):

    def __init__(self, clips: List[AudioClip]):
        self.clips: List[AudioClip] = clips
        super().__init__()
