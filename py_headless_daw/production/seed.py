from random import randint, Random
from typing import Any, Dict, TypeVar

T = TypeVar('T')
RandomChoiceOptions = Dict[T, float]


class Seed:
    """
    A controllable random seed for all kinds of repeatable random uses

    Requirements:
      - similar seeds should produce similar outputs
      - ...
    """

    def __init__(self, seed: str = None):
        self._seed: str = seed
        self._generator: Random = Random(seed)

    def randint(self, min_val: int, max_val: int, sub_seed: str):
        local_generator = Random(self._seed + sub_seed)
        return local_generator.randint(min_val, max_val)

    def choose_one(self, sub_seed: str, probabilities: RandomChoiceOptions) -> T:
        return list(probabilities.keys())[0]  # dummy impl
