from py_headless_daw.schema.events.event import Event


class MidiEvent(Event):

    MIDI_TYPE_REGULAR = 1
    MIDI_TYPE_SYSEX = 2

    @property
    def type(self):
        return self.TYPE_MIDI

    def __init__(self, sample_position: int):
        Event.__init__(self, sample_position)

        self.midi_event_type: int = self.MIDI_TYPE_REGULAR
        self.status: int = 0
        self.data1: int = 0
        self.data2: int = 0
        self.note: int = -1
        self.channel: int = 1

    def is_note_off(self) -> bool:
        # we consider any event with velocity == 0 as note off, which can be not correct sometimes,
        # but is enough for now
        if self.data2 == 0:
            return True

        return False

    def is_note_on(self) -> bool:
        # in fact it's much more complex than this, but it's ok for now
        return self.data2 != 0

    @property
    def velocity(self) -> int:
        return self.data2

    @velocity.setter
    def velocity(self, new_velocity: int):
        self.data2 = new_velocity

    @property
    def note(self) -> int:
        return self.data1

    @note.setter
    def note(self, new_note: int):
        self.data1 = new_note
