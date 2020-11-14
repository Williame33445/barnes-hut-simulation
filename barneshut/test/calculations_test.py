import unittest

from barneshut.calculations import *

class Gravityest(unittest.TestCase):

    def test_CalculateGravity(self):
        p00 = particle(1, 0, 0)
        p01 = particle(1, 0, 1)
        p10 = particle(1, 1, 0)
        p11 = particle(1, 1, 1)

        g0 = calculateGravitationalForce(p01, p01)
        self.assertEquals(0, g0.x)
        self.assertEquals(0, g0.y)

        g1 = calculateGravitationalForce(p00, p01)
        self.assertEquals(0, g1.x)
        self.assertEquals(g, g1.y)

        g2 = calculateGravitationalForce(p00, p10)
        self.assertEquals(g, g2.x)
        self.assertEquals(0, g2.y)

        expected = g / math.sqrt(2)**3
        g3 = calculateGravitationalForce(p00, p11)
        self.assertEquals(expected, g3.x)
        self.assertEquals(expected, g3.y)

        g4 = calculateGravitationalForce(p11, p00)
        self.assertEquals(-expected, g4.x)
        self.assertEquals(-expected, g4.y)

        bigP11 = particle(4.0, 1, 1)
        bigP00 = particle(5.0, 0, 0)
        bigExpected = -expected * bigP11.mass * bigP00.mass
        g5 = calculateGravitationalForce(bigP11, bigP00)
        self.assertEquals(bigExpected, g5.x)
        self.assertEquals(bigExpected, g5.y)