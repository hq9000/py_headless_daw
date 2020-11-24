from typing import cast

from py_headless_daw.shared.having_name import HavingName
from py_headless_daw.project.having_parameters import HavingParameters


class Plugin(HavingParameters, HavingName):
    def configure_with_preset(self, preset) -> None:
        from py_headless_daw.project.plugins.plugin_preset import PluginPreset  # to avoid a cyclic load time dependency
        preset = cast(PluginPreset, preset)
        for parameter in preset.parameters:
            val_from_preset = preset.get_parameter_value(parameter.name)
            self.set_parameter_value(parameter.name, val_from_preset)
