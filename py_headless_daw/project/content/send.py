from py_headless_daw.project.having_parameters import HavingParameters
from py_headless_daw.project.track import Track


class Send(HavingParameters):
    PARAM_GAIN: str = 'gain'
    PARAM_PANNING: str = 'panning'

    TYPE_PRE_CHAIN: str = 'pre'
    TYPE_POST_CHAIN: str = 'post'

    def __init__(self, source: Track, target: Track):
        super().__init__()

        self.source: Track = source
        self.target: Track = target
        self.type = self.TYPE_POST_CHAIN

        self.add_parameter(self.PARAM_GAIN, 1.0)
        self.add_parameter(self.PARAM_PANNING, 0.0)
