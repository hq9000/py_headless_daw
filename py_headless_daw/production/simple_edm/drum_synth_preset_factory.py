from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.project.plugins.plugin_preset import PluginPreset


class SimpleEdmDrumSynthPresetFactory:
    def create_bd_preset(self) -> PluginPreset:
        res = PluginPreset()
        return res

    def generate_bd_preset(self, seed: str) -> PluginPreset:
        res = PluginPreset('standard bd', DrumSynthPlugin)


