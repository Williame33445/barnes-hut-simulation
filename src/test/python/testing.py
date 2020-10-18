import sys
import os
sys.path.append(os.path.abspath("src/main/python"))

from tree import *

def printTree(t,depth=0):
    print(depth*" " + "center=(" + str(t.midPoint.x)+","+str(t.midPoint.y)+")" + ",halfWidth=" +
    str(t.halfWidth) + ",numberOfChildren=" + str(t.particleCount-1))
    for x in range(t.particleCount):
        if t.children[x] != None:
            printTree(t.children[x],depth+1)


lst = [particle(1.0,-3.0,-3.0),particle(1.0,-2.0,-3.0)]

def buildTree(lst,rootNode):
    for x in range(len(lst)):
        rootNode.addParticle(lst[x])
    printTree(rootNode)

rootNode = Node(Position(0,0),5)
buildTree(lst,rootNode)
rootNode.findMassDistribution()
print(rootNode.mass)

#change names at some
