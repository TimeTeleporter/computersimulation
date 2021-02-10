from typing import List
import numpy as np
from random import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from vectors import randomDirection
import particle
import domain

class Experiment():
    """A class to implement the experiment setup. It takes care of the time aspect."""
    def __init__(self, volume, particles: List[particle.Particle], numberOfSimulationSteps):
        self.volume: domain.Volume = volume
        self.particles = particles
        self.numberOfSimulationSteps = numberOfSimulationSteps
        self.stepIndex = 1
    
    def getParticlePositions(self):
        """Returns a np.array with the particle position vectors in each row."""
        return np.array([particle.position for particle in self.particles])
    
    def runStep(self):
        #print(self.stepIndex)
        for particle in self.particles:
            particle.move()
            self.volume.reflectParticle(particle)
            self.stepIndex += 1
            #particle.showState()
    
    def run(self):
        while self.stepIndex < self.numberOfSimulationSteps:
            self.runStep()

class Cube2DExperiment(Experiment):
    def __init__(self, volume: domain.Cuboid, particles: List[particle.Particle]):
        super().__init__(volume, particles, 1)
        self.volume: domain.Cuboid = volume
    
    def runAnimated2D(self):
        if not self.volume.dimensions == 2:
            print("Please only animate 2D Particles!")
            return 1
        
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.volume.vector[0])
        ax.set_ylim(0, self.volume.vector[1])
        circles, = ax.plot([], [], 'bo', ms=6)

        def animationFunction(i):
            xdata, ydata = np.transpose(self.getParticlePositions())
            self.runStep()
            circles.set_data(xdata, ydata)
            return circles,
        
        animation = FuncAnimation(fig, func=animationFunction, frames=600, interval=10, blit=True)
        plt.show()
    
    def createCube2DExperiment(cubeEdgeLength, numberOfParticles, particleMass, maxSpeed):
        NUMBER_OF_DIMENSIONS=2
        cube = domain.Cuboid(np.array([abs(cubeEdgeLength) for i in range(NUMBER_OF_DIMENSIONS)]))
        particles = []
        for i in range(numberOfParticles):
            part = particle.Particle(cube.randomPosition(), maxSpeed * random(), randomDirection(NUMBER_OF_DIMENSIONS), particleMass)
            part.showState()
            particles.append(part)
        return Cube2DExperiment(cube, particles)

exp = Cube2DExperiment.createCube2DExperiment(100, 10, 1, 1)
exp.runAnimated2D()