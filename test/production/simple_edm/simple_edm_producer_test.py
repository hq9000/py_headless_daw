import unittest

from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.simple_edm_producer import SimpleEdmProducer


class MyTestCase(unittest.TestCase):
    def test_something(self):
        producer = SimpleEdmProducer()
        seed = Seed('hello')
        res = producer.generate_project(seed)


if __name__ == '__main__':
    unittest.main()
