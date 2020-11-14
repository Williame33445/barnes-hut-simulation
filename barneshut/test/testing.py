import sys
import os
sys.path.append(os.path.abspath("."))

from barneshut.tree import *


def printTree(t,depth=0):
    print(depth*" " + "center=(" + str(t.midPoint.x)+","+str(t.midPoint.y)+")" + ",halfWidth=" +
    str(t.halfWidth) + ",numberOfChildren=" + str(t.particleCount-1))
    for c in t.children():
        printTree(c,depth+1)


lst = [particle(1.0,-3.0,-3.0),particle(1.0,-2.0,-3.0)]

def buildTree(lst,rootNode):
    for x in range(len(lst)):
        rootNode.addParticle(lst[x])
    printTree(rootNode)

rootNode = Node(Vector(0,0),5)
buildTree(lst,rootNode)
rootNode.findMassDistribution()
print(rootNode.combinedParticle)
"""look at vector class with acceleration,velocity and dispalcement subclasses"""
