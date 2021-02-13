from typing import List
import numpy as np
from vectors import randomDirection
import particle
import domain
import multiprocessing as mp

def handleParticleMovement(particle: particle.Particle, volume: domain.Volume):
    particle.move()
    volume.reflectParticle(particle)
    impulse = volume.getAndResetImpulse()
    return particle, impulse

class Experiment():
    """A class to implement the experiment setup. It takes care of the time aspect."""
    def __init__(self, volume, particles: List[particle.Particle], pool: mp.Pool):
        self.pool = pool
        self.volume: domain.Volume = volume
        self.particles = particles
        self.impulseStack = 0
        self.time: int = 0
    
    def handleParticleCollisions(self):
        for i in range(len(self.particles)):
            for j in np.arange(i, len(self.particles)):
                if i != j and particle.checkCollision(self.particles[i], self.particles[j]):
                    particle.collision(self.particles[i], self.particles[j])
    
    def updatePressure(self, impulses):
        impulseHeap = sum(impulses)
        self.impulseStack = self.impulseStack + (impulseHeap / self.volume.surfaceArea - self.impulseStack) / self.time
    
    def runStep(self, iterations=1):
        for i in range(iterations):
            self.time += 1
            #print(str(self.time))            
            particleAndImpulse = [self.pool.apply(handleParticleMovement, args=(particle, self.volume)) for particle in self.particles]   
            self.particles, impulses = [[x[i] for x in particleAndImpulse] for i in range(len(particleAndImpulse[0]))]
            self.updatePressure(impulses)
            self.handleParticleCollisions()
            #self.showPressure()
    
    def calculateEnergy(self):
        self.energy = 0
        for part in self.particles:
            part.showState()
            self.energy += part.speed * part.speed * part.mass / 2
        print("System energy:", str(self.energy))
        return self.energy
    
    def showPressure(self):
        print("System pressure:", str(self.impulseStack/self.time))
    
    def showState(self):
        self.calculateEnergy()
        if self.time != 0: self.showPressure()
    
    def createParticleList(numberofParticles, volume: domain.Volume, speed, mass, radius):
        return [particle.Particle(volume.randomPosition(), speed, randomDirection(volume.dimensions), mass, radius) for x in range(numberofParticles)]