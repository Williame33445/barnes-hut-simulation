import sys
import os
sys.path.append(os.path.abspath("."))

from barneshut.tree import *
def buildTree(lst,rootNode):
    for x in range(len(lst)):
        rootNode.addParticle(lst[x])


lst = [particle(1.0,-3.0,-3.0),particle(1.0,-2.0,-3.0),particle(4.0,-2.0,-1.0),particle(4.0,-3.0,-3.5),particle(7.0,-2.0,1.0),particle(1.0,2.0,-3.0)] #data
rootNode = Node(Vector(0,0),50)
buildTree(lst,rootNode)

rootNode.findMassDistribution()
a = []
for x in lst:
    acc = rootNode.calculateNetAcceleration(x)
    print(str(acc.x) + "," + str(acc.y))