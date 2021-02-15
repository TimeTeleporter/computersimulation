import timing
import numpy as np
from scipy.constants import k, u, value, milli
from experiment import Experiment
from domain import Cuboid

"""
1. Ideal gas law
We create an experiment with 1000 particles in a 3 dimensional cube with kinetic energy of 300 Kelvin.
"""

N = 100 # Number of particles
m = 2 * u # kg
r = value('Bohr radius')
l = 1 #meter
f = 3 # Dimensions and degrees of freedom
T = 300 # Kelvin
v = np.sqrt(2 * k * T / m)

print("Initial energy:", str(N * k * T), "J")
print("Initial speed:", str(v))

cube = Cuboid([l for dim in range(f)])

def speedFunction(): return v

print("Ideal pressure:", str(N * k * T / cube.setVolume()), "J/m**3") # N = 100, T = 300 K, V = 1 m**3, p = N * k * T / V

exp = Experiment(cube, Experiment.createParticleList(N, cube, speedFunction, m, r), milli)
exp.showState()
exp.runStep(5000)
exp.showState()