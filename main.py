import numpy as np
from experiment import Experiment
from domain import Cuboid

"""
1. Ideal gas law
We create an experiment with 1000 particles in a 3 dimensional cube with kinetic energy of 300 Kelvin.
"""

N = 100 # Number of particles
l = 100 # Edge length of the cube
dimensions = 3
v, m, r = 1, 1, 1 # Initial particle speed, mass and radius

cube = Cuboid(np.array([l for dim in range(dimensions)]))
def speedFunction() -> float: return v

print("Initial energy:", str(N * m * v * v * 0.5)) # Kinetic energy sum E = N k T
print("Expected pressure:", str(N * m * v * v * 0.5 / cube.setVolume()))

exp = Experiment(cube, Experiment.createParticleList(N, cube, speedFunction, m, r))
exp.showState()
exp.speedHisotgram()
exp.runStep(10)
exp.speedHisotgram()
exp.runStep(100)
exp.speedHisotgram()
exp.runStep(1000)
exp.speedHisotgram()
exp.runStep(1000)
exp.speedHisotgram()
exp.runStep(1000)
exp.speedHisotgram()
exp.runStep(1000)
exp.speedHisotgram()
exp.showState()