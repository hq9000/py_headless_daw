from typing import List

from py_headless_daw.project.having_parameters import HavingParameters
from py_headless_daw.project.parameter import Parameter, ParameterValueType, ParameterRangeType
from py_headless_daw.project.plugins.internal_plugin import GainPlugin, PanningPlugin
from py_headless_daw.project.plugins.plugin import Plugin
from py_headless_daw.project.project import Track


class AudioTrack(Track):
    GAIN: str = 'gain'
    PANNING: str = 'panning'

    def __init__(self):
        super().__init__()
        self._plugins: List[Plugin] = []
        self._gain: GainPlugin = GainPlugin()
        self._panner: PanningPlugin = PanningPlugin()

    @HavingParameters.parameters.getter  # type: ignore
    def parameters(self):
        return self._gain.parameters + self._panner.parameters

    def add_parameter(self, name: str,
                      value: ParameterValueType,
                      param_type: str,
                      value_range: ParameterRangeType):
        raise Exception('adding parameters to this object is not supported')

    def get_gain_parameter(self) -> Parameter:
        return self._gain.get_parameter(GainPlugin.PARAMETER_GAIN)

    def get_panning_parameter(self) -> Parameter:
        return self._panner.get_parameter(PanningPlugin.PARAMETER_PANNING)

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
