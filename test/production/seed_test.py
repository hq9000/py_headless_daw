import unittest

from py_headless_daw.production.seed import Seed


class MyTestCase(unittest.TestCase):
    def test_choose_one(self):
        seed = Seed('hello world')
        choice = seed.choose_one('whatever', {
            'hello': 10
        })
        self.assertEqual('hello', choice)

    def test_randint(self):
        seed = Seed('seed1')

        res = seed.randint(0, 10000, "subseed1")
        self.assertEqual(4872, res)

        res = seed.randint(0, 10000, "subseed1")
        self.assertEqual(4872, res)

        res = seed.randint(0, 10000, "subseed2")
        self.assertEqual(6248, res)

        seed = Seed('seed2')

        res = seed.randint(0, 10000, "subseed1")
        self.assertEqual(898, res)


if __name__ == '__main__':
    unittest.main()
