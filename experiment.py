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
        self.pressure = 0
        self.time: int = 0
        self.particleIndexCombinations = []
        for i in range(len(self.particles)):
            for j in np.arange(i+1, len(self.particles)):
                self.particleIndexCombinations.append((i,j))
    
    def updatePressure(self, impulses):
        dt = 1
        impulseHeap = sum(impulses)
        # incremental average where (impulseHeap / (self.volume.surfaceArea * dt) is the pressure during one timestep.
        self.pressure = self.pressure + (impulseHeap / (self.volume.surfaceArea * dt) - self.pressure) / self.time
    
    def doParallelCollisions(self, particles, list):
        partilcesAndIndices = [self.pool.apply(particle.collision, args=(particles[i], particles[j], i, j)) for (i, j) in list]
        for (p1, p2, i, j) in partilcesAndIndices:
            particles[i] = p1
            particles[j] = p2
        return particles
    
    def coordinateParallelCollisions(self):
        isCollidedList = [self.pool.apply(particle.checkCollision, args=(self.particles[i], self.particles[j])) for (i, j) in self.particleIndexCombinations]
        collisionIndexList = [x for i, x in enumerate(self.particleIndexCombinations) if isCollidedList[i]]
        while collisionIndexList != []:
            doCollisionList = [] # List of tuples for the next round of parallel collision calculations
            index = 0
            doCollisionList.append(collisionIndexList.pop(index))
            collisionCheckSet = set(doCollisionList)
            while index < len(collisionIndexList):
                checkSet = set(collisionIndexList[index])
                if bool(collisionCheckSet.intersection(checkSet)): # When one particle already undergoes collision
                    index += 1
                else:
                    collisionCheckSet.union(checkSet)
                    doCollisionList.append(collisionIndexList.pop(index))
            self.particles = self.doParallelCollisions(self.particles, doCollisionList)
    
    def runStep(self, iterations=1):
        for i in range(iterations):
            self.time += 1
            particleAndImpulse = [self.pool.apply(handleParticleMovement, args=(particle, self.volume)) for particle in self.particles]
            self.particles, impulses = [[x[i] for x in particleAndImpulse] for i in range(len(particleAndImpulse[0]))]
            self.updatePressure(impulses)
            self.coordinateParallelCollisions()
            print(self.time)
    
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
        if self.time != 0: self.showPressure()
    
    def createParticleList(numberofParticles, volume: domain.Volume, speed, mass, radius):
        return [particle.Particle(volume.randomPosition(), speed, randomDirection(volume.dimensions), mass, radius) for x in range(numberofParticles)]