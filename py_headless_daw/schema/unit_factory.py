from em.platform.rendering.processing_strategies.stream.mixer import Mixer
from em.platform.rendering.processing_strategies.hybrid.vst_plugin import VstPlugin
from em.platform.rendering.schema.host import Host
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy

from em.platform.rendering.schema.unit import Unit


class UnitFactory:

    def __init__(self, host: Host):
        self.host = host

    def create_tal_bassline(self) -> Unit:
        return self.create_standard_synth('TAL-BassLine.dll')

    def create_synth1(self) -> Unit:
        return self.create_standard_synth('Synth1.dll')

    # noinspection PyMethodMayBeStatic
    def create_reverb4(self) -> Unit:
        strategy: ProcessingStrategy = VstPlugin('TAL-Reverb-4.dll')
        res: Unit = Unit(2, 0, 2, 0, self.host, strategy)
        return res

    # noinspection PyMethodMayBeStatic
    def create_mixer(self, stream_ins: int, stream_outs: int) -> Unit:
        strategy: ProcessingStrategy = Mixer()
        res: Unit = Unit(stream_ins, 0, stream_outs, 0, self.host, strategy)
        return res

    def create_standard_synth(self, dll_name: str) -> Unit:
        strategy: ProcessingStrategy = VstPlugin(dll_name)
        res: Unit = Unit(0, 1, 2, 0, self.host, strategy)
        return res
