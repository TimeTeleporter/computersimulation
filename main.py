from scipy.constants import k, u, value
import multiprocessing as mp
from experiment import Experiment
from domain import Cuboid

"""
1. Ideal gas law
We create an experiment with 1000 particles in a 3 dimensional cube with kinetic energy of 300 Kelvin.
"""

N = 1000 # Number of particles
m = 2 * u
r = value('Bohr radius')
l = 1
f = 3 # Dimensions and degrees of freedom
T = 300 # Kelvin
v = 2 * k * T / m

cube = Cuboid([1 for dim in range(f)])

if __name__ == '__main__': # protect your program's entry point
    pool = mp.Pool(mp.cpu_count())
    exp = Experiment(cube, Experiment.createParticleList(N, cube, v / 10**9, m, r), pool)
    exp.showState()
    exp.runStep(1000)
    exp.showState()