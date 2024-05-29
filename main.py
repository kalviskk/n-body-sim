# %%
import numpy as np
import timeit
import matplotlib.pyplot as plt
import pickle
import signal
from simulate import simulate
from emptyDir import empty_directory
from createParticles import createParticles
from generateVideo import generateMP4
from BHTree import *

np.random.seed(2)

# initialize
N = 2000  # number of particles
total_steps = 10000
G = 1  # gravitational constant (some value to keep mass low)
dt = 1  # time step
height = 500
width = 500
distribution = "ring"
ring_radius = 600  # Radius of the ring


def save_particles(particles, filename="particles.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(particles, f)
    print("Particles array saved.")


def signal_handler(sig, frame):
    save_particles(particles)
    print("Simulation interrupted. Particles array saved.")
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

empty_directory("simulation")
particles = createParticles(N, height, width, G, ring_radius, 100, distribution)
start = timeit.default_timer()
simulate(particles, dt, total_steps, height, width)
stop = timeit.default_timer()

save_particles(particles)  # Save particles at the end of the simulation

timePerStep = (stop - start) / total_steps
print(f"time for each step: {timePerStep:.3f} s")
print(f"time for simulation: {(stop - start):.2f} s")
print(f"steps per second: {1/timePerStep}")
generateMP4()
