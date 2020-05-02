from em.platform.rendering.processing_strategies.event.abc.abstract_stateless_event_processor import \
    AbstractStatelessEventProcessor
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.events.midi_event import MidiEvent


class EventTransposer(AbstractStatelessEventProcessor):

    def __init__(self, transpose: int):
        self._transpose = transpose

    def _process_event(self, e: Event, buffer_length: int):

        if e.get_event_type() == Event.TYPE_MIDI:
            midi_event: MidiEvent = e
            if midi_event.is_note_on() or midi_event.is_note_off():
                midi_event.set_note(midi_event.get_note() + self._transpose)
