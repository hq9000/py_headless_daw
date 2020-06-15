from typing import List

from py_headless_daw.project.having_parameters import HavingParameters
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin
from py_headless_daw.project.plugins.plugin import Plugin
from py_headless_daw.project.project import Track


class AudioTrack(Track):
    GAIN: str = 'gain'
    PANNING: str = 'panning'

    def __init__(self):
        super().__init__()
        self._plugins: List[Plugin] = []
        self._gain: InternalPlugin = InternalPlugin(InternalPlugin.TYPE_GAIN)
        self._panner: InternalPlugin = InternalPlugin(InternalPlugin.TYPE_PANNING)

    @HavingParameters.parameters.getter
    def parameters(self):
        return self._gain.parameters + self._panner.parameters

    def add_parameter(self, name: str, value: float):
        raise Exception('adding parameters to this object is not supported')

    @property
    def plugins(self) -> List[Plugin]:
        return self._plugins + [
            self._gain,
            self._panner
        ]

    @plugins.setter
    def plugins(self, plugins: List[Plugin]):
        self._plugins = []
        for plugin in plugins:
            self._plugins.append(plugin)
