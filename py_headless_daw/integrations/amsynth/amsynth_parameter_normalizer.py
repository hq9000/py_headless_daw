from typing import List

kAmsynthParameter_AmpEnvAttack = 0
kAmsynthParameter_AmpEnvDecay = 1
kAmsynthParameter_AmpEnvSustain = 2
kAmsynthParameter_AmpEnvRelease = 3
kAmsynthParameter_Oscillator1Waveform = 4
kAmsynthParameter_FilterEnvAttack = 5
kAmsynthParameter_FilterEnvDecay = 6
kAmsynthParameter_FilterEnvSustain = 7
kAmsynthParameter_FilterEnvRelease = 8
kAmsynthParameter_FilterResonance = 9
kAmsynthParameter_FilterEnvAmount = 10
kAmsynthParameter_FilterCutoff = 11
kAmsynthParameter_Oscillator2Detune = 12
kAmsynthParameter_Oscillator2Waveform = 13
kAmsynthParameter_MasterVolume = 14
kAmsynthParameter_LFOFreq = 15
kAmsynthParameter_LFOWaveform = 16
kAmsynthParameter_Oscillator2Octave = 17
kAmsynthParameter_OscillatorMix = 18
kAmsynthParameter_LFOToOscillators = 19
kAmsynthParameter_LFOToFilterCutoff = 20
kAmsynthParameter_LFOToAmp = 21
kAmsynthParameter_OscillatorMixRingMod = 22
kAmsynthParameter_Oscillator1Pulsewidth = 23
kAmsynthParameter_Oscillator2Pulsewidth = 24
kAmsynthParameter_ReverbRoomsize = 25
kAmsynthParameter_ReverbDamp = 26
kAmsynthParameter_ReverbWet = 27
kAmsynthParameter_ReverbWidth = 28
kAmsynthParameter_AmpDistortion = 29
kAmsynthParameter_Oscillator2Sync = 30
kAmsynthParameter_PortamentoTime = 31
kAmsynthParameter_KeyboardMode = 32
kAmsynthParameter_Oscillator2Pitch = 33
kAmsynthParameter_FilterType = 34
kAmsynthParameter_FilterSlope = 35
kAmsynthParameter_LFOOscillatorSelect = 36
kAmsynthParameter_FilterKeyTrackAmount = 37
kAmsynthParameter_FilterKeyVelocityAmount = 38
kAmsynthParameter_AmpVelocityAmount = 39
kAmsynthParameter_PortamentoMode = 40
kAmsynthParameterCount = 41


# 	enum class Law {
# 		kLinear,		// offset + base * value
# 		kExponential,	// offset + base ^ value
# 		kPower			// offset + value ^ base
# 	};

class AmsynthParameterLaw:
    EXPONENTIAL = 'exponential'
    POWER = 'power'
    LINEAR = 'linear'


# typedef enum {
# 	KeyboardModePoly,
# 	KeyboardModeMono,
# 	KeyboardModeLegato,
# } KeyboardMode;
#
# typedef enum {
# 	PortamentoModeAlways,
# 	PortamentoModeLegato
# } PortamentoMode;

KeyboardModePoly = 0
KeyboardModeMono = 1
KeyboardModeLegato = 2

PortamentoModeAlways = 0
PortamentoModeLegato = 1

# 	enum class Type {
# 		kLowPass,
# 		kHighPass,
# 		kBandPass,
# 		kBandStop,
# 		kBypass
# 	};
#
# 	enum class Slope {
# 		k12,
# 		k24,
# 	};

kLowPass = 0
kHighPass = 1
kBandPass = 2
kBandStop = 3
kBypass = 4

k12 = 0
k24 = 2


class AmsynthParameter:

    # 					Parameter		(const std::string &name = "unused", Param id = kAmsynthParameterCount,
    # 									 float value = 0.0, float min = 0.0, float max = 1.0, float inc = 0.0,
    # 									 Law law = Law::kLinear, float base = 1.0, float offset = 0.0,
    # 									 const std::string &label = "");

    def __init__(self, name: str = "unused",
                 param_id: int = kAmsynthParameterCount,
                 default: float = 0.0,
                 min_val: float = 0.0,
                 max_val: float = 1.0,
                 inc: float = 0.0,
                 law: str = AmsynthParameterLaw.LINEAR,
                 base: float = 1.0, offset: float = 0.0,
                 label: str = ""):
        self.name: str = name
        self.id: int = param_id
        self.min: float = min_val
        self.max: float = max_val
        self.inc: float = inc
        self.default: float = default
        self.law: str = law
        self.base: float = base
        self.offset: float = offset
        self.label: str = label


class AmsynthTimeParameter(AmsynthParameter):
    def __init__(self, name: str, param_id: int):
        super().__init__(name=name, param_id=param_id, min_val=0.0, max_val=2.5,
                         default=0.0, inc=0.0,
                         law=AmsynthParameterLaw.POWER,
                         base=3, offset=0.0005,
                         label="s")


class AmsynthParameterNormalizer:
    """
    This class converts Amsynth parameter values from bank files into [0..1] ranges to be accepted as vst param values
    """

    def __init__(self):
        self._parameters: List[AmsynthParameter] = [
            AmsynthTimeParameter("amp_attack", kAmsynthParameter_AmpEnvAttack),
            AmsynthTimeParameter("amp_decay", kAmsynthParameter_AmpEnvDecay),
            AmsynthParameter("amp_sustain", kAmsynthParameter_AmpEnvSustain, 1),
            AmsynthTimeParameter("amp_release", kAmsynthParameter_AmpEnvRelease),
            AmsynthParameter("osc1_waveform", kAmsynthParameter_Oscillator1Waveform, 2, 0, 4, 1),
            AmsynthTimeParameter("filter_attack", kAmsynthParameter_FilterEnvAttack),
            AmsynthTimeParameter("filter_decay", kAmsynthParameter_FilterEnvDecay),
            AmsynthParameter("filter_sustain", kAmsynthParameter_FilterEnvSustain, 1),
            AmsynthTimeParameter("filter_release", kAmsynthParameter_FilterEnvRelease),
            AmsynthParameter("filter_resonance", kAmsynthParameter_FilterResonance, 0, 0, 0.97),
            AmsynthParameter("filter_env_amount", kAmsynthParameter_FilterEnvAmount, 0, -16, 16),
            AmsynthParameter("filter_cutoff", kAmsynthParameter_FilterCutoff, 1.5, -0.5, 1.5, 0,
                             AmsynthParameterLaw.EXPONENTIAL, 16, 0),
            AmsynthParameter("osc2_detune", kAmsynthParameter_Oscillator2Detune, 0, -1, 1, 0,
                             AmsynthParameterLaw.EXPONENTIAL, 1.25, 0),
            AmsynthParameter("osc2_waveform", kAmsynthParameter_Oscillator2Waveform, 2, 0, 4, 1),
            AmsynthParameter("master_vol", kAmsynthParameter_MasterVolume, 0.67, 0, 1, 0, AmsynthParameterLaw.POWER, 2,
                             0),
            AmsynthParameter("lfo_freq", kAmsynthParameter_LFOFreq, 0, 0, 7.5, 0, AmsynthParameterLaw.POWER, 2, 0,
                             "Hz"),
            AmsynthParameter("lfo_waveform", kAmsynthParameter_LFOWaveform, 0, 0, 6, 1),
            AmsynthParameter("osc2_range", kAmsynthParameter_Oscillator2Octave, 0, -3, 4, 1,
                             AmsynthParameterLaw.EXPONENTIAL, 2, 0),
            AmsynthParameter("osc_mix", kAmsynthParameter_OscillatorMix, 0, -1, 1),
            AmsynthParameter("freq_mod_amount", kAmsynthParameter_LFOToOscillators, 0, 0, 1.25992105, 0,
                             AmsynthParameterLaw.POWER, 3, -1),
            AmsynthParameter("filter_mod_amount", kAmsynthParameter_LFOToFilterCutoff, -1, -1, 1),
            AmsynthParameter("amp_mod_amount", kAmsynthParameter_LFOToAmp, -1, -1, 1),
            AmsynthParameter("osc_mix_mode", kAmsynthParameter_OscillatorMixRingMod, 0, 0, 1, 0),
            AmsynthParameter("osc1_pulsewidth", kAmsynthParameter_Oscillator1Pulsewidth, 1),
            AmsynthParameter("osc2_pulsewidth", kAmsynthParameter_Oscillator2Pulsewidth, 1),
            AmsynthParameter("reverb_roomsize", kAmsynthParameter_ReverbRoomsize),
            AmsynthParameter("reverb_damp", kAmsynthParameter_ReverbDamp),
            AmsynthParameter("reverb_wet", kAmsynthParameter_ReverbWet),
            AmsynthParameter("reverb_width", kAmsynthParameter_ReverbWidth, 1),
            AmsynthParameter("distortion_crunch", kAmsynthParameter_AmpDistortion, 0, 0, 0.9),
            AmsynthParameter("osc2_sync", kAmsynthParameter_Oscillator2Sync, 0, 0, 1, 1),
            AmsynthParameter("portamento_time", kAmsynthParameter_PortamentoTime, 0.0, 0.0, 1.0),
            AmsynthParameter("keyboard_mode", kAmsynthParameter_KeyboardMode, KeyboardModePoly, 0, KeyboardModeLegato,
                             1),
            AmsynthParameter("osc2_pitch", kAmsynthParameter_Oscillator2Pitch, 0, -12, +12, 1),
            AmsynthParameter("filter_type", kAmsynthParameter_FilterType, kLowPass, kLowPass, kBypass, 1),
            AmsynthParameter("filter_slope", kAmsynthParameter_FilterSlope, k24, k12, k24, 1),
            AmsynthParameter("freq_mod_osc", kAmsynthParameter_LFOOscillatorSelect, 0, 0, 2, 1),
            AmsynthParameter("filter_kbd_track", kAmsynthParameter_FilterKeyTrackAmount, 1),
            AmsynthParameter("filter_vel_sens", kAmsynthParameter_FilterKeyVelocityAmount, 1),
            AmsynthParameter("amp_vel_sens", kAmsynthParameter_AmpVelocityAmount, 1),
            AmsynthParameter("portamento_mode", kAmsynthParameter_PortamentoMode, PortamentoModeAlways)
        ]

    def normalize(self, param_name: str, denormalized_value: float):
        param = self._find_param_by_name(param_name)
        normalized_value = (denormalized_value - param.min) / (param.max - param.min)

        if normalized_value < 0 or normalized_value > 1:
            raise ValueError(
                f'{param_name}: normalized value of {normalized_value} derived from denormalized_value={denormalized_value} is outside [0.0, 1.0] range (error: ce350d7b)')

        return normalized_value

    def denormalize(self, param_name: str, normalized_value: float) -> float:
        if normalized_value < 0 or normalized_value > 1:
            raise ValueError(
                f'{param_name}: normalized value {normalized_value} is outside [0.0, 1.0] range (error: ce350d7b)')

        param = self._find_param_by_name(param_name)
        return param.min + (param.max - param.min) * normalized_value

    def _find_param_by_name(self, param_name: str) -> AmsynthParameter:
        for parameter in self._parameters:
            if parameter.name == param_name:
                return parameter

        raise ValueError(f'unable to find an amsynth parameter named {param_name} (error: 71c9a67c)')
