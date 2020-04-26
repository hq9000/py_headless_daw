import unittest

import numpy as np

from py_headless_daw.processing.stream.constant_level import ConstantLevel
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit


class ConstantLevelStrategyTest(unittest.TestCase):
    def test_smoke(self):
        host = Host()
        strategy = ConstantLevel(np.float32(0.50))
        unit = Unit(0, 0, 1, 0, host, strategy)

        all_output_nodes = unit.get_all_output_nodes()

        self.assertEqual(1, len(all_output_nodes))

        output_node = all_output_nodes[0]

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1

        out_buffer = np.ndarray(shape=(100,), dtype=np.float32)
        output_node.render(interval, out_buffer)

        for x in range(0, 100):
            self.assertEqual(0.5, out_buffer[x])


if __name__ == '__main__':
    unittest.main()
