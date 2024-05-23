# %%
import numpy as np
import timeit
import matplotlib.pyplot as plt
from simulate import simulate
from emptyDir import empty_directory
from createParticles import createParticles
from generateVideo import generateMP4
from BHTree import BHTree

np.random.seed(2)

# initialize
N = 5000  # number of particles
total_steps = 200000
G = 0.5  # gravitational constant (some value to keep mass low)
dt = 0.5  # time step
height = 300
width = 300
distribution = "ring"
ring_radius = 200  # Radius of the ring
ring_width = 2  # Width of the ring

empty_directory("simulation")
particles = createParticles(N, height, width, G, ring_radius, 100, "ring")
start = timeit.default_timer()
simulate(particles, G, dt, total_steps, height, width)
stop = timeit.default_timer()


timePerStep = (stop - start) / total_steps
print(f"time for each step: {timePerStep:.3f} s")
print(f"time for simulation: {(stop - start):.2f} s")
print(f"steps pre second: {1/timePerStep}")
generateMP4()
