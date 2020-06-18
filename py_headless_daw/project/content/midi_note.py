from py_headless_daw.project.content.midi_clip_event import MidiClipEvent


class MidiNote(MidiClipEvent):
    LENGTH_TIMING_CLIP: str = 'clip'
    LENGTH_TIMING_ABSOLUTE: str = 'absolute'

    def __init__(self, clip_time: float, note: int, velocity: int, length: float):
        super().__init__(clip_time)
        self.note: int = note
        self.velocity: int = velocity
        self.length: float = length
        self.length_timing: str = self.LENGTH_TIMING_CLIP

    def get_absolute_time_of_note_off(self) -> float:
        pass
