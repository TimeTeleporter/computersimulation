import numpy as np
from vectors import magnitude, normalize, combilize

class Particle():
    """Models the behaviour of a particle."""
    def __init__(self, position, speed, direction, mass, radius):
        self.position = position
        self.speed = speed
        self.direction = direction
        self.mass = mass
        self.radius = radius
        self.numberOfCollisions = 0
    
    def showState(self):
        print(self.position, self.speed, self.direction)
    
    def move(self):
        self.position = self.position + self.speed * self.direction
    
    def getImpulseVector(self):
        return self.mass * self.speed * self.direction

def checkCollision(particle1: Particle, particle2: Particle):
    """Returns True if the two particles collided."""
    distance = magnitude(particle1.position - particle2.position)
    if distance < particle1.radius + particle2.radius and distance > magnitude(particle1.position + particle1.direction - particle2.position - particle2.direction):
        return True
    return False

def collision(particle1: Particle, particle2: Particle):
    xrel = particle2.position - particle1.position
    # We shift the impulse space to give the particle2 zero impulse and save particle 1 in p1.
    impulseShift = particle2.getImpulseVector()
    p1 = particle1.getImpulseVector() - impulseShift
    p2neu = normalize(xrel) * np.dot(p1, xrel) / magnitude(xrel)
    particle1.speed, particle1.direction = combilize((p1 - p2neu + impulseShift) / particle1.mass)
    particle2.speed, particle2.direction = combilize((p2neu + impulseShift) / particle2.mass)
    particle1.numberOfCollisions += 1
    particle2.numberOfCollisions += 1