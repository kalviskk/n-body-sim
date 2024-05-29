import numpy as np
import timeit
from simulate import simulate
from emptyDir import empty_directory
from createParticles import createParticles
from generateVideo import generateMP4
from BHTree import *

# Set random seed for reproducibility
np.random.seed(2)

# Initialize parameters
N = 2000  # number of particles
total_steps = 100  # number of simulation steps
G = 1  # gravitational constant
dt = 1  # time step
height = 500  # height of the simulation area
width = 500  # width of the simulation area
distribution = "ring"  # particle distribution type
ring_radius = 600  # radius of the ring distribution

# Empty the simulation directory
empty_directory("simulation")
# Create particles
particles = createParticles(N, height, width, G, ring_radius, 100, distribution)
# Start the simulation timer
start = timeit.default_timer()
# Run the simulation
simulate(particles, dt, total_steps, height, width)
# Stop the simulation timer
stop = timeit.default_timer()
# Calculate and print simulation time statistics
timePerStep = (stop - start) / total_steps
print(f"time for each step: {timePerStep:.3f} s")
print(f"time for simulation: {(stop - start):.2f} s")
print(f"steps per second: {1/timePerStep}")
print(N)
# Generate video from simulation images
generateMP4()
