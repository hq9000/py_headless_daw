from py_headless_daw.schema.events.midi_event import MidiEvent


class MidiEventFactory:
    SAMPLE_POSITION_UNDEFINED: int = -1

    STATUS_TEMPLATE_NOTE_ON: int = 0b10010000
    STATUS_TEMPLATE_NOTE_OFF: int = 0b10000000
    STATUS_TEMPLATE_PROGRAM_CHANGE: int = 0b11000000

    def __init__(self):
        self.channel_number: int = 0
        pass

    def create_note_on_event(self, note: int, velocity: int, position: int = SAMPLE_POSITION_UNDEFINED) -> MidiEvent:
        status_byte: int = self.STATUS_TEMPLATE_NOTE_ON
        status_byte += self.channel_number

        data1: int = note
        data2: int = velocity

        event = MidiEvent(position)

        event.status = status_byte
        event.data1 = data1
        event.data2 = data2

        event.note = note
        return event

    def create_note_off_event(self, note: int, velocity: int, position: int = SAMPLE_POSITION_UNDEFINED) -> MidiEvent:
        return self.create_note_on_event(note=note, velocity=0, position=position)
