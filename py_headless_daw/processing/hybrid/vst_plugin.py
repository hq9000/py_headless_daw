from typing import List

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy
import em.platform.adapters.vst_wrapper.vst_plugin as wrapper


class VstPlugin(ProcessingStrategy):

    def __init__(self, plugin_name: str):
        self.plugin_name: str = plugin_name
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
