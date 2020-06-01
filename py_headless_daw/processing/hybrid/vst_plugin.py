from typing import List

import numpy as np

from cython_vst_loader.vst_event import VstMidiEvent, VstNoteOnMidiEvent, VstNoteOffMidiEvent
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin as InternalPlugin
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event import MidiEvent
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from py_headless_daw.schema.unit import Unit


class VstPlugin(ProcessingStrategy):

    def __init__(self, path_to_plugin_file: bytes, unit: Unit):
        super().__init__()
        self.unit = unit
        self._path_to_plugin_file: bytes = path_to_plugin_file

        bpm = self.unit.host.bpm
        sample_rate = self.unit.host.sample_rate
        buffer_size = self.unit.host.block_size

        host = VstHost(int(sample_rate), buffer_size)
        host.bpm = bpm
        self._internal_plugin: InternalPlugin = InternalPlugin(path_to_plugin_file, host)

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        midi_events: List[Event] = self._filter_events(event_inputs, Event.TYPE_MIDI)

        internal_midi_events = map(self._convert_midi_event_to_internal, midi_events)
        if len(midi_events) > 0:
            # noinspection PyTypeChecker
            self._internal_plugin.process_events(internal_midi_events)

        def numpy_array_to_pointer(numpy_array: np.ndarray) -> int:
            if numpy_array.ndim != 1:
                raise Exception('expected a 1d numpy array here')
            pointer, ro_flag = numpy_array.__array_interface__['data']
            return pointer

        input_stream_pointers: List[int] = []
        output_stream_pointers: List[int] = []

        block_size: int = stream_outputs[0].shape[0]
        for stream_input in stream_inputs:
            if stream_input.shape[0] != block_size:
                raise Exception('block of different unexpected size')
            input_stream_pointers.append(numpy_array_to_pointer(stream_input))

        for stream_output in stream_outputs:
            if stream_output.shape[0] != block_size:
                raise Exception('block of different unexpected size')
            output_stream_pointers.append(numpy_array_to_pointer(stream_output))

        self._internal_plugin.process_replacing(input_stream_pointers, output_stream_pointers, block_size)

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
