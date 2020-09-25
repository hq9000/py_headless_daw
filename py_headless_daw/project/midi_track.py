from typing import List

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.midi_clip import MidiClip, MidiClipEvent
from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.project import Track


class MidiTrack(Track):

    def __init__(self, channel: int):
        super().__init__()
        self.channel: int = channel
        self.clips: List[MidiClip] = []

    def add_output(self, output: Track):
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

        clips = self._find_overlapping_clips(start_time, end_time)
        res: List[MidiClipEvent] = []

        for clip in clips:
            events = self._find_overlapping_events(clip, start_time, end_time)
            for event in events:
                res.append(event)

        return res

    def _find_overlapping_clips(self, start_time: float, end_time: float) -> List[MidiClip]:
        """
        http://i.imgur.com/HpSAG4P.png

        :param start_time:
        :param end_time:
        :return:
        """
        res: List[MidiClip] = []
        for clip in self.clips:
            overlaps: bool = True
            if clip.end_time < start_time:
                overlaps = False
            if clip.start_time >= end_time:
                # http://i.imgur.com/BJI5ol6.png
                overlaps = False

            if overlaps:
                res.append(clip)

        return res

    @staticmethod
    def _find_overlapping_events(clip: MidiClip, start_time: float, end_time: float) -> List[MidiClipEvent]:
        res: List[MidiClipEvent] = []
        tolerance: float = 0.0000001
        for event in clip.events:
            overlaps: bool = True
            if event.get_absolute_start_time() >= end_time - tolerance:
                overlaps = False
            if event.get_absolute_end_time() < start_time + tolerance:
                overlaps = False
            if overlaps:
                res.append(event)

        return res
