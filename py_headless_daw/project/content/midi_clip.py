from typing import Sequence

from py_headless_daw.project.content.clip import Clip


class MidiClip(Clip):
    def __init__(self, start_time: float, end_time: float):
        super().__init__(start_time, end_time)
        from py_headless_daw.project.content.midi_note import MidiNote  # to avoid an import-time loop
        self.midi_notes: Sequence[MidiNote] = []

    @property
    def events(self):
        # type: ()->Sequence[MidiClipEvent]
        return self.midi_notes


class MidiClipEvent:

    LENGTH_TIMING_CLIP_RELATIVE: str = 'clip'
    LENGTH_TIMING_ABSOLUTE: str = 'absolute'

    def __init__(self, clip, clip_time):
        # type: (MidiClip, float) -> None
        self.clip_time: float = clip_time
        self.clip: MidiClip = clip
        self.timing = self.LENGTH_TIMING_CLIP_RELATIVE

    def get_absolute_start_time(self) -> float:
        return self.clip.start_time + self.clip_time * self.clip.length_in_seconds

    def get_absolute_end_time(self) -> float:
        return self.get_absolute_start_time()
