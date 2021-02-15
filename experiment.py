from typing import List
import numpy as np
import matplotlib.pyplot as plt
from vectors import randomDirection
import particle
import domain

class Experiment():
    """A class to implement the experiment setup. It takes care of the time aspect."""
    def __init__(self, volume, particles: List[particle.Particle], secondsPerStep=1):
        self.volume = volume
        self.particles = particles
        self.secondsPerStep = secondsPerStep
        for particle in self.particles: particle.speed = particle.speed * self.secondsPerStep
        self.pressure = 0
        self.time: int = 0
    
    def moveParticles(self):
        for part in self.particles:
            part.move()
            self.volume.reflectParticle(part)
    
    def handleParticleCollisions(self):
        for i in range(len(self.particles)):
            for j in np.arange(i, len(self.particles)):
                if i != j and particle.checkCollision(self.particles[i], self.particles[j]):
                    particle.collision(self.particles[i], self.particles[j])
    
    def updatePressure(self):
        impulseHeap = 0
        for boundry in self.volume.boundries:
            impulseHeap += boundry.absorbedImpulse
            boundry.absorbedImpulse = 0
        dt = self.secondsPerStep
        self.pressure = self.pressure + (impulseHeap / (self.volume.surfaceArea * dt * dt) - self.pressure) / self.time
    
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
            #part.showState()
            self.energy += part.speed * part.speed * part.mass / (2 * self.secondsPerStep * self.secondsPerStep)
        print("System energy:", str(self.energy))
        return self.energy
    
    def showPressure(self):
        print("System pressure:", str(self.pressure))
    
    def showState(self):
        self.calculateEnergy()
        if self.time != 0: self.showPressure()
    
    def speedHisotgram(self, binmode='auto'):
        speedlst = [part.speed for part in self.particles]
        if binmode != 'auto': binmode=np.arange(0,max(speedlst), 1.1 * min(speedlst))
        fig = plt.hist(speedlst, bins=binmode)
        plt.title("Speed distribution at step " + str(self.time))
        plt.show()
    
    def createParticleList(numberofParticles, volume: domain.Volume, speedfunc, mass, radius):
        return [particle.Particle(volume.randomPosition(), speedfunc(), randomDirection(volume.dimensions), mass, radius) for x in range(numberofParticles)]