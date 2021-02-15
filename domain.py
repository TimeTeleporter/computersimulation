from typing import List
from particle import Particle
import numpy as np
from random import random
from abc import ABC, abstractmethod

class Boundry(ABC):
    """An abstract class for what a boundry should do."""
    def __init__(self):
        self.absorbedImpulse = 0
    
    @abstractmethod
    def check(self, vector):
        """Returns True if the boundry is violated."""
        return False
    
    @abstractmethod
    def reflectPosition(self, vector):
        """Returns the Vector reflected at the wall."""
        return vector
    
    @abstractmethod
    def reflectDirection(self, vector):
        """Returns a reflected direction vector."""
        return vector
    
    @abstractmethod
    def updateImpulse(self, particle: Particle):
        """Each boundry saves and updates the total impulse experienced by collided particles. This then gets red and reset every timestep by a function in the Experiment class."""
        pass
    
    def reflectParticle(self, particle: Particle):
        """Reflects a particle on the boundry."""
        particle.position = self.reflectPosition(particle.position)
        particle.direction = self.reflectDirection(particle.direction)
        self.updateImpulse(particle)

class Wall(Boundry):
    """Implements a boundry of a cuboid volume."""
    def __init__(self, dimension, modifier, position):
        self.dimension = dimension
        self.modifier = modifier
        self.position = position
        super().__init__()
    
    def check(self, vector):
        """Returns True if the given vector is outside the wall."""
        if vector[self.dimension] * self.modifier > self.position:
            return True
        return False
    
    def reflectPosition(self, vector):
        """Returns the vector reflected at the wall."""
        newVector = vector
        newVector[self.dimension] = 2 * self.position - newVector[self.dimension]
        return newVector
    
    def reflectDirection(self, vector):
        """Reflects the vector in the direction of the wall at the wall."""
        newVector = vector
        newVector[self.dimension] = -1 * newVector[self.dimension]
        return newVector
    
    def updateImpulse(self, particle: Particle):
        """Saves the experienced impulse."""
        self.absorbedImpulse += 2 * particle.mass * particle.speed * abs(particle.direction[self.dimension])
        return self.absorbedImpulse

class Volume(ABC):
    """An abstract class that coordinates boundries and holds measurements."""
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.setBoundries()
        self.setSurfaceArea()
        self.setVolume()
    
    @abstractmethod
    def setBoundries(self):
        """A method that needs to be implemented to make a list self.boundries of boundry class objects."""
        self.boundries: List[Boundry] = []
    
    @abstractmethod
    def setSurfaceArea(self):
        """A method  that needs to be implemented to return the surface area of the volume."""
        self.surfaceArea = 1*self.dimensions #or something
    
    @abstractmethod
    def setVolume(self):
        self.volume = 0
    
    @abstractmethod
    def randomPosition(self):
        """A method  that needs to be implemented to return a random position inside the volume."""
        pass
    
    def checkBoundries(self, position):
        """Returns True if a boundry is violated."""
        for boundry in self.boundries:
            if boundry.check(position):
                return True
        return False
    
    def reflectParticle(self, particle: Particle):
        """Reflects position and direction of a given particle."""
        while self.checkBoundries(particle.position):
            for boundry in self.boundries:
                if boundry.check(particle.position):
                    boundry.reflectParticle(particle)

class Cuboid(Volume):
    """A class that implements the abstract volume in a cuboid shape. See that
    it inherits some functions from its parent class. The cuboid spans form the
    origin to the point of its vector 'self.vector', with its edges oriented othogonally."""
    def __init__(self, vector):
        self.vector = vector
        super().__init__(len(self.vector))
    
    def setBoundries(self):
        WALL_LEFT=-1
        WALL_RIGHT=1
        self.boundries: List[Wall] = []
        for index in range(self.dimensions):
            self.boundries.append(Wall(index, WALL_LEFT, 0))
            self.boundries.append(Wall(index, WALL_RIGHT, self.vector[index]))
    
    def setSurfaceArea(self):
        array = []
        for boundry in self.boundries:
            area = 1
            for index in range(self.dimensions):
                if index != boundry.dimension:
                    area *= self.vector[index]
            array.append(area)
        self.surfaceArea = sum(array)
        return self.surfaceArea
    
    def setVolume(self):
        self.volume = np.prod(self.vector)
        return self.volume
    
    def randomPosition(self):
        array = []
        for index in range(self.dimensions):
            array.append(self.vector[index] * random())
        return np.array(array)