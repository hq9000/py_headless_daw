from ctypes import c_int, sizeof
from typing import List, Callable, Union, Optional, Iterator

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event import MidiEvent
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from pyvst import VstPlugin as PyvstPlugin
from pyvst.midi import midi_note_as_bytes, wrap_vst_events
from pyvst.vstwrap import VstMidiEvent as PyvstMidiEvent, VstEventTypes


class VstPlugin(ProcessingStrategy):

    def __init__(self, path_to_plugin: str, host_callback: Callable = None):
        self._path_to_plugin: str = path_to_plugin
        self._host_callback: Optional[Callable] = None
        if host_callback is not None:
            self._host_callback = host_callback

        self._pyvst_plugin: PyvstPlugin = PyvstPlugin(path_to_plugin, host_callback)

    def render(self, interval: TimeInterval, stream_inputs: np.ndarray, stream_outputs: np.ndarray,
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        """

        :param interval:
        :param stream_inputs:
        :param stream_outputs:
        :param event_inputs:
        :param event_outputs:
        :return:
        """

        num_input_channels: int
        input_sample_frames: int
        num_input_channels, input_sample_frames = stream_inputs.shape

        num_output_channels: int
        output_sample_frames: int
        num_output_channels, output_sample_frames = stream_outputs.shape

        assert input_sample_frames == output_sample_frames

        flattened_events: List[Event] = self._flatten_event_inputs(event_inputs)

        pyvst_events: List[PyvstMidiEvent] = self._transform_events_to_pyvst_events(flattened_events)

        wrapped_events = wrap_vst_events(pyvst_events)

        self._pyvst_plugin.process_events(wrapped_events)
        self._pyvst_plugin.process(stream_inputs, input_sample_frames)  # todo

    def _transform_events_to_pyvst_events(self, native_events: List[Event]) -> List[PyvstMidiEvent]:
        res = []
        for native_event in native_events:
            # only MidiEvents are supposed to be fed to VSTs
            if isinstance(native_event, MidiEvent):
                res.append(self._convert_native_event_to_pyvst_event(native_event))
        return res

    @staticmethod
    def _convert_native_event_to_pyvst_event(native_event: MidiEvent) -> PyvstMidiEvent:

        midi_data = bytes([
            native_event.type,
            native_event.data1,
            native_event.data2,
        ])

        return PyvstMidiEvent(
            type=VstEventTypes.kVstMidiType,
            byte_size=sizeof(PyvstMidiEvent),
            delta_frames=c_int(native_event.get_sample_position()),
            flags=0,
            note_length=0,
            note_offset=0,
            midi_data=midi_data,
            detune=0,
            note_off_velocity=0
        )
