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
    """
    A class representing a midi event

    A midi clip event is an instant (zero length) something that is characterized by the time of its onset.
    There are two ways to translate clip times to wall clock times:

    TIMING_TYPE_CLIP_RELATIVE - the time offset from the beginning of the clips is calculated
    proportionally to the length of the clip

    TIMING_TYPE_CLIP_ABSOLUTE - the time offset from the beginning of the clips is
    taken directly as number of seconds (float) to pass from the beginning of the clip.
    """
    TIMING_TYPE_CLIP_RELATIVE: str = 'timing_clip_relative'
    TIMING_TYPE_CLIP_ABSOLUTE: str = 'timing_clip_absolute'

    def __init__(self, clip, clip_time):
        # type: (MidiClip, float) -> None
        self.clip_time: float = clip_time
        self.clip: MidiClip = clip
        self.timing_type: str = self.TIMING_TYPE_CLIP_RELATIVE

    def get_absolute_start_time(self) -> float:
        if self.timing_type == self.TIMING_TYPE_CLIP_ABSOLUTE:
            time_relative_to_clip = self.clip_time
        elif self.timing_type == self.TIMING_TYPE_CLIP_RELATIVE:
            time_relative_to_clip = self.clip_time * self.clip.length_in_seconds
        else:
            raise ValueError(f'start timing type of {self.timing_type} is not supported (error: 864e96c0)')

        return self.clip.start_time + time_relative_to_clip

    def get_absolute_end_time(self) -> float:
        return self.get_absolute_start_time()
