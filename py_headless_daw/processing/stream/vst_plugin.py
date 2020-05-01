from typing import List, Callable, Union, Optional

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from pyvst import VstPlugin as PyvstPlugin

class VstPlugin(ProcessingStrategy):

    def __init__(self, path_to_plugin: str, host_callback: Callable = None):
        self._path_to_plugin: str = path_to_plugin
        self._host_callback: Optional[Callable] = None
        if host_callback is not None:
            self._host_callback = host_callback

        self._pyvst_pluging =


    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        pass
