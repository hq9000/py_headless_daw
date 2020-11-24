import unittest

from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.simple_edm_producer import SimpleEdmProducer


class MyTestCase(unittest.TestCase):
    def test_something(self):
        seed = Seed('hello')
        producer = SimpleEdmProducer(seed)
        res = producer.generate_project()


if __name__ == '__main__':
    unittest.main()
