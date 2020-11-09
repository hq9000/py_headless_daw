from py_headless_daw.project.plugins.internal_plugin import InternalPlugin


class DrumSynth(InternalPlugin):

    PARAM_NAME_OSC1_WAVEFORM

    def __init__(self):
        super().__init__()

        self.add_parameter()