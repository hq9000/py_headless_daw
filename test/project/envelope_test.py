import unittest

from py_headless_daw.project.envelope import Envelope, EnvelopePoint
from py_headless_daw.project.parameter import Parameter


class EnvelopeTest(unittest.TestCase):
    def test_envelope(self):
        target = Parameter('a', 0.777, Parameter.TYPE_FLOAT, (0.0, 1.0))
        envelope = Envelope(target)

        point1 = EnvelopePoint(0.0, 0.0)
        point2 = EnvelopePoint(1.0, 10.0)

        envelope.points = [point2, point1]

        self.assertEqual(0.0, envelope.get_value(0.0))
        self.assertEqual(5, envelope.get_value(0.5))
        self.assertEqual(10, envelope.get_value(1.0))
        self.assertEqual(0, envelope.get_value(-1.0))
        self.assertEqual(10, envelope.get_value(2.0))
