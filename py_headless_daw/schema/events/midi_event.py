from em.platform.rendering.schema.events.event import Event


class MidiEvent(Event):
    TYPE_REGULAR = 1
    TYPE_SYSEX = 2
    SIZE_META = 3

    def __init__(self, sample_position: int):
        Event.__init__(self, sample_position)
        self.type: int = self.TYPE_REGULAR
        self.status: int = 0
        self.data1: int = 0
        self.data2: int = 0
        self.note: int = -1

    def get_type(self) -> str:
        return Event.TYPE_MIDI

    def is_note_off(self) -> bool:
        # we consider any event with velocity == 0 as note off, which can be not correct sometimes,
        # but is enough for now
        if self.data2 == 0:
            return True

        return False

    def is_note_on(self) -> bool:
        # in fact it's much more complex than this, but it's ok for now
        return self.data2 != 0

    def get_velocity(self) -> int:
        return self.data2

    def set_note(self, note: int):
        self.data1 = note

    def get_note(self) -> int:
        return self.data1
