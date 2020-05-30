from typing import List
from cython_vst_loader.vst_host import VstHost
import numpy as np

from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class VstPlugin(ProcessingStrategy):

    def __init__(self, path_to_plugin_file: bytes):
        self.plugin_name: str = plugin_name
        host = VstHost(self)
        self._plugin: wrapper.VstPlugin = wrapper.VstPlugin(plugin_name)

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        midi_events: List[Event] = self._filter_events(event_inputs, Event.TYPE_MIDI)

        if len(midi_events) > 0:
            # noinspection PyTypeChecker
            self._plugin.process_midi_events(midi_events)

        self._plugin.process_audio(stream_inputs, stream_outputs)

    def get_plugin(self) -> wrapper.VstPlugin:
        return self._plugin
