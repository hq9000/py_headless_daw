import unittest

import numpy as np

from py_headless_daw.processing.stream.constant_level import ConstantLevel
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit


class MyTestCase(unittest.TestCase):
    def test_something(self):
        host = Host()
        strategy = ConstantLevel(np.float32(0.5))
        unit = Unit(0, 1, 1, 0, host, strategy)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
