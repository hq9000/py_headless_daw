from em.platform.rendering.processing_strategies.stream.impulse_noice_generator import ImpulseNoiseGeneratorStrategy
from em.platform.rendering.schema.unit import Unit


class ImpulseNoiseGenerator(Unit):
    def __init__(self):
        processing_strategy = ImpulseNoiseGeneratorStrategy()

        super(ImpulseNoiseGenerator, self).__init__(0, 0, 2, 0, processing_strategy)
