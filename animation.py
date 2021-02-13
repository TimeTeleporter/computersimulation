from typing import List
import numpy as np
from random import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from vectors import randomDirection
import particle
import domain
import multiprocessing as mp
from experiment import Experiment

class Cube2DExperiment(Experiment):
    def __init__(self, volume: domain.Cuboid, particles: List[particle.Particle], pool):
        super().__init__(volume, particles, pool)
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
            self.runStep()
            xdata, ydata = np.transpose([particle.position for particle in self.particles])
            circles.set_data(xdata, ydata)
            return circles,
        
        animation = FuncAnimation(fig, func=animationFunction, interval=10, blit=True)
        plt.show()
    
    @classmethod
    def createCube2DExperiment(exp, cubeEdgeLength, numberOfParticles, particleMass, maxSpeed, particleRadius, pool):
        NUMBER_OF_DIMENSIONS=2
        cube = domain.Cuboid(np.array([abs(cubeEdgeLength) for i in range(NUMBER_OF_DIMENSIONS)]))
        particles = Experiment.createParticleList(numberOfParticles, cube, maxSpeed * random(), particleMass, particleRadius)
        return exp(cube, particles, pool)

if __name__ == '__main__': # protect your program's entry point
    pool = mp.Pool(mp.cpu_count())
    exp: Cube2DExperiment = Cube2DExperiment.createCube2DExperiment(100, 1000, 1, 1, 1, pool)
    exp.showState()
    exp.runAnimated2D()
    exp.showState()