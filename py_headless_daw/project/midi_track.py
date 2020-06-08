from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.project import Track
from py_headless_daw.project.synth_track import SynthTrack


class MidiTrack(Track):
    def __init__(self, channel: int):
        super().__init__()
        self.channel: int = channel

    def add_output(self, output: SynthTrack):
        if not isinstance(output, SynthTrack):
            raise RoutingException('attempted to set an output of a midi track to a non-synth track')
        super().add_output(output)
