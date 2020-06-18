from py_headless_daw.project.content.midi_clip import MidiClip


class MidiClipEvent:
    def __init__(self, clip, clip_time):
        # type: (MidiClip, float) -> None
        self.clip = clip  # type: MidiClip
        self.clip_time: float = clip_time

    def get_absolute_time(self) -> float:
        pass