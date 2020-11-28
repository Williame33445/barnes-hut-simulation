import sys
import os
sys.path.append(os.path.abspath("."))

from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *

halfWidth = 50
tickDuration = 2
duration = 10
numberOfCycles = int(duration/tickDuration)

particles = [KinematicParticle(1.0,Vector(1.0,-3.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(1.0,-2.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(4.0,-2.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(4.0,-3.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(7.0,-2.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(1.0,2.0),Vector(1.0,1.0))]

simulator = Simulator(particles,halfWidth)

for z in range(numberOfCycles):
    for p in particles:
        print(str(p))
    print("-------")
    simulator.tick(tickDuration)
