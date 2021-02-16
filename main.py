import numpy as np
from experiment import Experiment
from domain import Cuboid

N = 250 # Number of particles
l = 100 # Edge length of the cube
dimensions = 3
v, m, r = 1, 1, 1 # Initial particle speed, mass and radius

cube = Cuboid(np.array([l for dim in range(dimensions)]))
def speedFunction() -> float: return v

print("Initial energy:", str(N * m * v * v * 0.5)) # Kinetic energy sum E = N k T
print("Expected pressure:", str(N * m * v * v * 0.5 / cube.setVolume()))

exp = Experiment(cube, Experiment.createParticleList(N, cube, speedFunction, m, r))
exp.showState()
exp.speedHisotgram(np.arange(0, 5, 0.2))
while exp.getCollisions() < 10: exp.runStep()
exp.speedHisotgram(np.arange(0, 5, 0.2))
while exp.getCollisions() < 100: exp.runStep()
exp.speedHisotgram(np.arange(0, 5, 0.2))
while exp.getCollisions() < 1000: exp.runStep()
exp.speedHisotgram(np.arange(0, 5, 0.2))
while exp.getCollisions() < 10000: exp.runStep()
exp.speedHisotgram(np.arange(0, 5, 0.2))
exp.showState()