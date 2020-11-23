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
        self.seed: str = seed

    def choose_one(self, area_code: str, probabilities: RandomChoiceOptions) -> T:
        return list(probabilities.keys())[0]  # dummy impl
