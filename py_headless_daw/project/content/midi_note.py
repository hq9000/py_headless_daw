from py_headless_daw.project.content.midi_clip import MidiClipEvent, MidiClip


class MidiNote(MidiClipEvent):
    LENGTH_TIMING_CLIP: str = 'clip'
    LENGTH_TIMING_ABSOLUTE: str = 'absolute'

    def __init__(self, clip, clip_time, note, velocity, length):
        # type: (MidiClip, float, int, int, float)->None
        super().__init__(clip, clip_time)
        self.note: int = note
        self.velocity: int = velocity
        self.length: float = length
        self.length_timing: str = self.LENGTH_TIMING_CLIP

    def get_absolute_end_time(self) -> float:
        return self.get_absolute_start_time() + self.length
