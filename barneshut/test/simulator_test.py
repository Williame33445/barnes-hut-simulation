from barneshut.simulator import Simulator
import unittest

from barneshut.particle import *

class SimulatorTest(unittest.TestCase):

    halfWidth = 50

    def test_singleParticleHasConstantVelocity(self):

        s0 = Vector(4.0,3.3)
        v = Vector(1.0,2.0)
        p = KinematicParticle(1.0,Vector(s0.x,s0.y),v)
        simulator = Simulator([p],self.halfWidth)

        tickDuration = 5
        for t in range(0,1000,tickDuration):
            self.assertEquals(f"mass=1.0,centre={str(s0.plus(v.times(t)))},velocity={str(v)}", str(p), f"t={str(t)}")
            simulator.tick(tickDuration)
