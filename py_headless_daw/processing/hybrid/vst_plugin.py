import logging
from typing import List, cast

import numpy as np

from cython_vst_loader.vst_event import VstMidiEvent, VstNoteOnMidiEvent, VstNoteOffMidiEvent
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin as InternalPlugin
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event import MidiEvent
from py_headless_daw.schema.events.parameter_value_event import ParameterValueEvent
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from py_headless_daw.schema.unit import Unit


class VstPlugin(ProcessingStrategy):

    def __init__(self, path_to_plugin_file: bytes, unit: Unit):
        super().__init__()
        self.unit: Unit = unit
        self._path_to_plugin_file: bytes = path_to_plugin_file

        bpm = self.unit.host.bpm
        sample_rate = self.unit.host.sample_rate
        buffer_size = self.unit.host.block_size

        host = VstHost(int(sample_rate), buffer_size)
        host.bpm = bpm
        self._internal_plugin: InternalPlugin = InternalPlugin(path_to_plugin_file, host)

    def set_parameter_value(self, name: str, value: float):
        param_idx = self._find_parameter_index_by_name(name)
        self._internal_plugin.set_parameter_value(param_idx, value)

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        # noinspection PyTypeChecker
        midi_events: List[MidiEvent] = cast(List[MidiEvent], self._filter_events(event_inputs, Event.TYPE_MIDI))

        # noinspection PyTypeChecker
        parameter_events: List[ParameterValueEvent] = cast(List[ParameterValueEvent],
                                                           self._filter_events(event_inputs,
                                                                               Event.TYPE_PARAMETER_VALUE)
                                                           )

        # just setting the values of params (if any corresponding events have arrived) before
        # processing the upcoming audio block.

        # this is a simple, and, probably, wrong approach to setting parameters to a plugin:
        # it does not allow to precisely put parameter change event with sample
        # accuracy, also, the behaviour of plugin starts to depend on the block size.
        for parameter_event in parameter_events:
            parameter_index: int = self._find_parameter_index_by_name(parameter_event.parameter_id)
            self._internal_plugin.set_parameter_value(parameter_index, parameter_event.value)

        internal_midi_events = list(map(self._convert_midi_event_to_internal, midi_events))

        assert interval.num_samples > 0, "num samples in this interval <= 0: " + str(
            interval.num_samples) + ", this cannot be right"

        if len(midi_events) > 0:
            logging.debug('processing events for unit %s in interval %i' % (self.unit.name, interval.id))

            assert self.midi_events_are_valid(interval, midi_events)
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

    def _find_parameter_index_by_name(self, parameter_string_id: str) -> int:
        """
        this method is used to convert from internal parameter ids (which are unique human-readable strings)
        into the indices of params of this particular vst plugin

        :param parameter_string_id:
        :return:
        """
        available_parameter_names: List[str] = []
        for idx in range(0, self._internal_plugin.get_num_parameters()):
            available_parameter_names.append(str(self._internal_plugin.get_parameter_name(idx)))
            if self._internal_plugin.get_parameter_name(idx) == parameter_string_id.encode('utf-8'):
                return idx

        raise LookupError(
            'a parameter named ' + str(parameter_string_id)
            + ' not found in this vst plugin. Available parameters are '
            + ", ".join(available_parameter_names))

    @staticmethod
    def midi_events_are_valid(interval: TimeInterval, midi_events: List[MidiEvent]) -> bool:
        for event in midi_events:
            if event.sample_position < 0:
                raise Exception('event has a negative sample position of ' + str(event.sample_position))
            if event.sample_position > interval.num_samples - 1:
                raise Exception(
                    'event has a too big sample position of ' + str(event.sample_position) + ". Max allowed is " + str(
                        interval.num_samples - 1)
                )

        return True
