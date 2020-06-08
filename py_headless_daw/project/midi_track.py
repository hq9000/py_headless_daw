from typing import List

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.project import Track


class MidiTrack(Track):
    def __init__(self, channel: int):
        super().__init__()
        self.channel: int = channel
        self.clips: List[MidiClip] = []

    def add_output(self, output: AudioTrack):
        if not isinstance(output, AudioTrack):
            raise RoutingException(
                'output of a midi track should be an audio track, instead attempted to use as output: ' + str(
                    type(output)))
        super().add_output(output)
