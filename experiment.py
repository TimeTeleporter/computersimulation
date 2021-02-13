from typing import List
import numpy as np
from vectors import randomDirection
import particle
import domain

class Experiment():
    """A class to implement the experiment setup. It takes care of the time aspect."""
    def __init__(self, volume, particles: List[particle.Particle]):
        self.volume: domain.Volume = volume
        self.particles = particles
        self.pressure = 0
        self.time: int = 0
    
    def moveParticles(self):
        for part in self.particles:
            part.move()
            self.volume.reflectParticle(part)
    
    def handleParticleCollisions(self):
        for i in range(len(self.particles)):
            for j in np.arange(i+1, len(self.particles)):
                if self.particles[i].checkCollision(self.particles[j]):
                    self.particles[i].collision(self.particles[j])
    
    def updatePressure(self):
        impulseHeap = 0
        for boundry in self.volume.boundries:
            impulseHeap += boundry.absorbedImpulse
            boundry.absorbedImpulse = 0
        self.pressure = self.pressure + (impulseHeap / self.volume.surfaceArea - self.pressure) / self.time
    
    def runStep(self, iterations=1):
        for i in range(iterations):
            self.time += 1
            #print(str(self.time))
            self.moveParticles()
            self.handleParticleCollisions()
            self.updatePressure()
            #self.showPressure()
    
    def calculateEnergy(self):
        self.energy = 0
        for part in self.particles:
            part.showState()
            self.energy += part.speed * part.speed * part.mass / 2
        print("System energy:", str(self.energy))
        return self.energy
    
    def showPressure(self):
        print("System pressure:", str(self.pressure))
    
    def showState(self):
        self.calculateEnergy()
        self.showPressure()
    
    def createParticleList(numberofParticles, volume: domain.Volume, speedfunc, mass, radius):
        return [particle.Particle(volume.randomPosition(), speedfunc(), randomDirection(volume.dimensions), mass, radius) for x in range(numberofParticles)]