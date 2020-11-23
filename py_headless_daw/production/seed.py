from random import randint, Random
from typing import Any, Dict, TypeVar

T = TypeVar('T')
RandomChoiceOptions = Dict[T, int]


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

    def choose_one(self, probabilities: RandomChoiceOptions, sub_seed: str) -> T:
        sum_of_probabilities: int = 0

        # probabilities do not have to sum up to 100 or anything,
        # it's enough if they are positive integers
        for option, add_probability in probabilities.items():
            sum_of_probabilities += add_probability

        dice_value = self.randint(0, sum_of_probabilities, sub_seed)

        sum_of_probabilities = 0
        for option, add_probability in probabilities.items():
            if sum_of_probabilities <= dice_value < sum_of_probabilities + add_probability:
                return option

        raise ValueError('unable to generate a random choice (error: 8256cd68)')


        return list(probabilities.keys())[0]  # dummy impl
