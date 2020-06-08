from typing import List

from py_headless_daw.project.content.clip import Clip
from py_headless_daw.project.content.midi_note import MidiNote


class MidiClip(Clip):
    def __init__(self, start_time: float, end_time: float):
        super().__init__(start_time, end_time)
        self.midi_notes: List[MidiNote] = []
