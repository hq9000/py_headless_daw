from typing import List

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_clip_event import MidiClipEvent
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

    def get_events(self, start_time: float, end_time: float) -> List[MidiClipEvent]:
        """
        Importantly, this method can return events that fall out to the left of the given time bracket
        because of the hanging notes:
        See ![image](https://user-images.githubusercontent.com/21345604/84991144-c93cec80-b14e-11ea-9053-a6763de8d1e2.png)


        :param start_time:
        :param end_time:
        :return:
        """
        return []
