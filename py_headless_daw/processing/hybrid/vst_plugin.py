from typing import List

import numpy as np

from cython_vst_loader.vst_event import VstMidiEvent, VstNoteOnMidiEvent, VstNoteOffMidiEvent
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin as InternalPlugin
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event import MidiEvent
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class VstPlugin(ProcessingStrategy):

    def __init__(self, path_to_plugin_file: bytes):
        super().__init__()
        self._path_to_plugin_file: bytes = path_to_plugin_file

        bpm = self.unit.host.bpm
        sample_rate = self.unit.host.sample_rate
        buffer_size = self.unit.host.block_size

        host = VstHost(int(sample_rate), buffer_size)

        self._internal_plugin: InternalPlugin = InternalPlugin(path_to_plugin_file, )

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        midi_events: List[Event] = self._filter_events(event_inputs, Event.TYPE_MIDI)

        internal_midi_events = map(self._convert_midi_event_to_internal, midi_events)
        if len(midi_events) > 0:
            # noinspection PyTypeChecker
            self._internal_plugin.process_events(internal_midi_events)

        # convert inputs/outputs into lists of pointers
        self._plugin.process_audio(stream_inputs, stream_outputs)


    @staticmethod
    def _convert_midi_event_to_internal(external_event: MidiEvent) -> VstMidiEvent:

        if not isinstance(external_event, MidiEvent):
            raise TypeError

        if external_event.is_note_on():
            res = VstNoteOnMidiEvent(
                external_event.get_sample_position(),
                external_event.note,
                external_event.velocity,
                external_event.channel
            )
        elif external_event.is_note_off():
            res = VstNoteOffMidiEvent(
                external_event.get_sample_position(),
                external_event.note,
                external_event.channel
            )
        else:
            raise TypeError('unknown external midi event type')

        return res
