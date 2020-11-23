import unittest

from py_headless_daw.production.seed import Seed


class MyTestCase(unittest.TestCase):
    def test_choose_one(self):
        seed = Seed('hello world')
        choice = seed.choose_one('whatever', {
            'hello': 10
        })
        self.assertEqual('hello', choice)


if __name__ == '__main__':
    unittest.main()
