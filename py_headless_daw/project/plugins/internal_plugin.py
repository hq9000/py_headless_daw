from typing import List

from py_headless_daw.project.plugins.plugin import Plugin


class InternalPlugin(Plugin):
    TYPE_GAIN: str = 'gain'
    TYPE_PANNING: str = 'panning'

    PARAMETER_GAIN: str = 'gain'
    PARAMETER_PANNING: str = 'panning'

    def __init__(self, plugin_type: str):
        self._validate_type(plugin_type)
        super().__init__()
        self.internal_plugin_type = plugin_type

        if plugin_type == self.TYPE_GAIN:
            self.add_parameter(self.PARAMETER_GAIN, 1.0)
        elif plugin_type == self.TYPE_PANNING:
            self.add_parameter(self.PARAMETER_PANNING, 0.0)
        else:
            raise Exception('unknown internal plugin type ' + plugin_type)

    def _validate_type(self, type_to_validate):
        available_types: List[str] = [
            self.TYPE_GAIN,
            self.TYPE_PANNING
        ]

        if type_to_validate not in available_types:
            raise Exception('only available types are: ' + ", ".join(available_types))
