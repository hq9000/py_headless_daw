from typing import Type

from py_headless_daw.project.having_parameters import HavingParameters
from py_headless_daw.project.plugins.plugin import Plugin


class PluginPreset(HavingParameters):

    def __init__(self, name: str,
                 plugin_class: Type[Plugin]):  # https://docs.python.org/3/library/typing.html#typing.Type
        self.name: str = name
        super().__init__()

        # instantiating a blank plugin instance
        plugin = plugin_class()

        for parameter_from_plugin in plugin.parameters:
            self.add_parameter_object(parameter_from_plugin)
