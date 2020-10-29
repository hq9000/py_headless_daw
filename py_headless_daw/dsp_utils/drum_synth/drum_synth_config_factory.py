from typing import List

from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator_config import DrumSynthGeneratorConfig


class DrumSynthConfigFactory:
    def get_all_preset_names(self) -> List[str]:
        pass

    def randomize(self, config: DrumSynthGeneratorConfig, temperature: float):
        pass
