from py_headless_daw.production.seed import Seed
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.project.plugins.plugin_preset import PluginPreset


class SimpleEdmDrumSynthPresetFactory:
    def create_bd_preset(self) -> PluginPreset:
        res = PluginPreset()
        return res

    def generate_bd_preset(self, seed: Seed) -> PluginPreset:
        res = PluginPreset('standard bd', DrumSynthPlugin)

        global_param_data = {
            DrumSynthPlugin.PARAM_NAME_NUM_OSCILLATORS: "1"
        }

        oscillator_param_data = {
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME: 1.0,
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_WAVEFORM: DrumSynthPlugin.PARAM_VALUE_WAVEFORM_SINE,
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_TIME: 0.01,
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_TIME: seed.randfloat(0.2, 0.3, "bd decay time"),
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_SUSTAIN_LEVEL: 0.0,
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_SUSTAIN_TIME: 0.0,
            DrumSynthPlugin.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_TIME: 0.0,
        }

        for name, value in global_param_data.items():
            res.set_parameter_value(name, value)

        for name_prefix, value in oscillator_param_data.items():
            param_name = DrumSynthPlugin.generate_param_name(name_prefix, 1)
            res.set_parameter_value(param_name, value)

        return res
