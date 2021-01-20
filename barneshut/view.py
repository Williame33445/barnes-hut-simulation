import cv2
import numpy as np

class ViewParams:
    def __init__(self,width,zoom,massFactor,particleColour=(100, 30, 30,),markerThickness=-1,backgroundValue=128):
        self.width = width
        self.zoom = zoom
        self.massFactor = massFactor
        self.particleColour = particleColour
        self.markerThickness = markerThickness
        self.backgroundValue = backgroundValue

        scaledWidth = self.scaled(width)
        self.scaledHalfWidth = round(scaledWidth / 2)
        self.frameShape = (scaledWidth, scaledWidth, 3) # width x height x three colours

    def scaled(self,v):
        return round(v * self.zoom)
    def scaledPos(self,particle):
        return (self.scaled(particle.pos.x) + self.scaledHalfWidth, self.scaled(particle.pos.y) + self.scaledHalfWidth)
    def scaledMass(self,particle):
        return round(particle.mass * self.massFactor)


class ViewCreator:
    def __init__(self,particles,params):
        self.particles = particles
        self.params = params

    def getCurrentView(self):
        frame = np.full(self.params.frameShape, self.params.backgroundValue, dtype=np.uint8)
        for p in self.particles:
            cv2.circle(frame, self.params.scaledPos(p), self.params.scaledMass(p), self.params.particleColour, self.params.markerThickness)

        return frame