# %%
import numpy as np
import timeit
from simulate import simulate
from emptyDir import empty_directory
from createParticles import createParticles
from generateVideo import generateMP4
from BHTree import *

np.random.seed(2)

# initialize
N = 2000  # number of particles
total_steps = 100
G = 1  # gravitational constant (some value to keep mass low)
dt = 1  # time step
height = 500
width = 500
distribution = "ring"
ring_radius = 600  # Radius of the ring


empty_directory("simulation")
particles = createParticles(N, height, width, G, ring_radius, 100, distribution)
start = timeit.default_timer()
simulate(particles, dt, total_steps, height, width)
stop = timeit.default_timer()

timePerStep = (stop - start) / total_steps
print(f"time for each step: {timePerStep:.3f} s")
print(f"time for simulation: {(stop - start):.2f} s")
print(f"steps per second: {1/timePerStep}")
print(N)
generateMP4()
