import unittest

from barneshut.particle import *

class VectorTest(unittest.TestCase):

    def test_vectorMaths(self):
        v0 = Vector(1.0,2.0)
        v1 = Vector(0.1,0.2)
        v2 = Vector(4.0,6.0)

        self.assertEquals("(1.1,2.2)", str(v0.plus(v1)))
        self.assertEquals("(0.9,1.8)", str(v0.minus(v1)))
        self.assertEquals("(2.0,4.0)", str(v0.times(2)))
        self.assertEquals("(0.5,1.0)", str(v0.dividedBy(2)))
        self.assertEquals(5.0, v0.distanceTo(v2))

        self.assertEquals("(1.0,2.0)", str(v0)) # Check that v0 is unchanged

        v0.translate(v1)
        self.assertEquals("(1.1,2.2)", str(v0)) # Check that v0 now changed

        # Other vectors sghould be unchanged
        self.assertEquals("(0.1,0.2)", str(v1))
        self.assertEquals("(4.0,6.0)", str(v2))


class ParticleTest(unittest.TestCase):

    def test_accelerationTowards(self):
        p00 = particle(1.0, 0.0, 0.0)
        p01 = particle(1.0, 0.0, 1.0)
        p10 = particle(1.0, 1.0, 0.0)
        p11 = particle(1.0, 1.0, 1.0)

        self.assertEquals("(0.0,0.0)", str(p00.accelerationTowards(p00)))
        self.assertEquals(f"(0.0,{G})", str(p00.accelerationTowards(p01)))
        self.assertEquals(f"({G},0.0)", str(p00.accelerationTowards(p10)))

        gRoot2 = G / math.sqrt(2.0)**3
        self.assertEquals(f"({gRoot2},{gRoot2})", str(p00.accelerationTowards(p11)))
        self.assertEquals(f"({-gRoot2},{-gRoot2})", str(p11.accelerationTowards(p00)))

        bigP11 = particle(4.0, 1.0, 1.0)
        bigP00 = particle(5.0, 0.0, 0.0)
        bigGRoot2 = -gRoot2 * bigP00.mass
        self.assertEquals(f"({bigGRoot2},{bigGRoot2})", str(bigP11.accelerationTowards(bigP00)))

    def test_combinedParticle(self):
        p0 = particle(mass=1.0,x=1.0,y=2.0)
        p1 = particle(mass=3.0,x=21.0,y=10.0)

        self.assertEquals("mass=1.0,centre=(1.0,2.0)",str(combinedParticle([p0])))
        self.assertEquals("mass=4.0,centre=(16.0,8.0)",str(combinedParticle([p0,p1])))

        # Original particles should be unchanged
        self.assertEquals("mass=1.0,centre=(1.0,2.0)", str(p0))
        self.assertEquals("mass=3.0,centre=(21.0,10.0)", str(p1))
