from typing import cast, List

from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator_config import DrumSynthGeneratorConfig, OscillatorConfig
from py_headless_daw.project.parameter import Parameter
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin
import inspect

DEFAULT_FREQUENCY_RANGE = 20_000


class DrumSynthPlugin(InternalPlugin):
    MAX_NUMBER_OF_OSCILLATORS = 4
    DEFAULT_ZERO_FREQUENCY = 10

    PARAM_VALUE_WAVEFORM_SINE = 'sine'
    PARAM_VALUE_WAVEFORM_SAWTOOTH = 'sawtooth'
    PARAM_VALUE_WAVEFORM_SQUARE = 'square'
    PARAM_VALUE_WAVEFORM_TRIANGLE = 'triangle'
    PARAM_VALUE_WAVEFORM_NOISE = 'noise'

    PARAM_NAME_NUM_OSCILLATORS = 'num_oscillators'

    PARAM_NAME_SUFFIX_OSCILLATOR_WAVEFORM = 'waveform'
    PARAM_NAME_SUFFIX_OSCILLATOR_WAVE_DISTORTION = 'wave_distortion'
    PARAM_NAME_SUFFIX_OSCILLATOR_ZERO_FREQUENCY = 'zero_frequency'
    PARAM_NAME_SUFFIX_OSCILLATOR_FREQUENCY_RANGE = 'frequency_range'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME = 'volume'

    PARAM_NAME_SUFFIX_OSCILLATOR_INITIAL_PHASE = 'initial_phase'

    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_TIME = 'volume_attack_time'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_CURVE_RATIO = 'volume_attack_curve_ratio'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_CURVE_POWER = 'volume_attack_curve_power'

    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_TIME = 'volume_decay_time'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_CURVE_RATIO = 'volume_decay_curve_ratio'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_CURVE_POWER = 'volume_decay_curve_power'

    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_SUSTAIN_LEVEL = 'sustain_level'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_SUSTAIN_TIME = 'sustain_time'

    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_TIME = 'volume_release_time'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_CURVE_RATIO = 'volume_release_curve_ratio'
    PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_CURVE_POWER = 'volume_release_curve_power'

    # pitch envelope parameters
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_ATTACK_TIME = 'pitch_attack_time'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_ATTACK_CURVE_RATIO = 'pitch_attack_curve_ratio'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_ATTACK_CURVE_POWER = 'pitch_attack_curve_power'

    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_DECAY_TIME = 'pitch_decay_time'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_DECAY_CURVE_RATIO = 'pitch_decay_curve_ratio'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_DECAY_CURVE_POWER = 'pitch_decay_curve_power'

    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_SUSTAIN_LEVEL = 'pitch_sustain_level'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_SUSTAIN_TIME = 'pitch_sustain_time'

    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_RELEASE_TIME = 'pitch_release_time'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_RELEASE_CURVE_RATIO = 'pitch_release_curve_ratio'
    PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_RELEASE_CURVE_POWER = 'pitch_release_curve_power'

    def __init__(self):

        super().__init__()

        self.add_parameter(name=self.PARAM_NAME_NUM_OSCILLATORS,
                           value="1",
                           param_type=Parameter.TYPE_ENUM,
                           value_range=[
                               "1", "2", "3", "4"
                           ])

        for i in range(1, self.MAX_NUMBER_OF_OSCILLATORS + 1):

            self.add_parameter(
                name=self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_WAVEFORM, i),
                value=self.PARAM_VALUE_WAVEFORM_SINE,
                param_type=Parameter.TYPE_ENUM,
                value_range=[
                    self.PARAM_VALUE_WAVEFORM_SINE,
                    self.PARAM_VALUE_WAVEFORM_SAWTOOTH,
                    self.PARAM_VALUE_WAVEFORM_SQUARE,
                    self.PARAM_VALUE_WAVEFORM_TRIANGLE,
                    self.PARAM_VALUE_WAVEFORM_NOISE
                ]
            )

            self.add_parameter(
                name=self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_ZERO_FREQUENCY, i),
                value=self.DEFAULT_ZERO_FREQUENCY,
                param_type=Parameter.TYPE_FLOAT,
                value_range=(0, 22050)
            )

            self.add_parameter(
                name=self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_FREQUENCY_RANGE, i),
                value=DEFAULT_FREQUENCY_RANGE,
                param_type=Parameter.TYPE_FLOAT,
                value_range=(0, 22050)
            )

            for member_name, prop in inspect.getmembers(type(self)):
                member_name = cast(str, member_name)
                if member_name.startswith('PARAM_NAME_SUFFIX_OSCILLATOR'):
                    param_name_suffix = getattr(self, member_name)
                    param_name = self.generate_param_name(param_name_suffix, i)
                    if not self.has_parameter(param_name):
                        value_range = (0.0, 1.0)
                        value = 0.5
                        self.add_parameter(param_name, value, Parameter.TYPE_FLOAT, value_range)

    def generate_generator_config(self) -> DrumSynthGeneratorConfig:
        osc_configs: List[OscillatorConfig] = []
        for i in range(1, int(self.get_parameter_value(self.PARAM_NAME_NUM_OSCILLATORS)) + 1):
            osc_config = OscillatorConfig(
                volume=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME, i)),
                zero_frequency=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_ZERO_FREQUENCY, i)),
                frequency_range=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_FREQUENCY_RANGE, i)),
                start_phase=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_INITIAL_PHASE, i)),
                wave_type=self.get_enum_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_WAVEFORM, i)),

                volume_envelope_attack_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_TIME, i)),
                volume_envelope_attack_curve_ratio=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_CURVE_RATIO, i)),
                volume_envelope_attack_curve_power=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_ATTACK_CURVE_POWER, i)),

                volume_envelope_decay_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_TIME, i)),
                volume_envelope_decay_curve_ratio=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_CURVE_RATIO, i)),
                volume_envelope_decay_curve_power=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_DECAY_CURVE_POWER, i)),

                volume_envelope_sustain_level=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_SUSTAIN_LEVEL, i)),
                volume_envelope_sustain_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_SUSTAIN_TIME, i)),

                volume_envelope_release_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_TIME, i)),
                volume_envelope_release_curve_ratio=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_CURVE_RATIO,
                                             i)),
                volume_envelope_release_curve_power=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_VOLUME_ENVELOPE_RELEASE_CURVE_POWER,
                                             i)),

                pitch_envelope_attack_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_ATTACK_TIME, i)),
                pitch_envelope_attack_curve_ratio=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_ATTACK_CURVE_RATIO, i)),
                pitch_envelope_attack_curve_power=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_ATTACK_CURVE_POWER, i)),

                pitch_envelope_decay_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_DECAY_TIME, i)),
                pitch_envelope_decay_curve_ratio=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_DECAY_CURVE_RATIO, i)),
                pitch_envelope_decay_curve_power=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_DECAY_CURVE_POWER, i)),

                pitch_envelope_sustain_level=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_SUSTAIN_LEVEL, i)),
                pitch_envelope_sustain_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_SUSTAIN_TIME, i)),

                pitch_envelope_release_time=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_RELEASE_TIME, i)),
                pitch_envelope_release_curve_ratio=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_RELEASE_CURVE_RATIO,
                                             i)),
                pitch_envelope_release_curve_power=self.get_float_parameter_value(
                    self.generate_param_name(self.PARAM_NAME_SUFFIX_OSCILLATOR_PITCH_ENVELOPE_RELEASE_CURVE_POWER,
                                             i))
            )

            osc_configs.append(osc_config)

        res = DrumSynthGeneratorConfig(osc_configs)

        return res

    @staticmethod
    def generate_param_name(suffix: str, oscillator_id: int) -> str:
        return suffix + '_osc' + str(oscillator_id)
