import matplotlib.pyplot as plt
from calc_accelerations import calculate_accelerations
from plotting import drawStep
from BHTree import *


def simulate(particles, dt, steps, height, width):
    fig, ax = plt.subplots()
    for step in range(int(steps)):
        if not step % 10:
            drawStep(particles, step, fig, ax, height, width)

        accelerations = calculate_accelerations(particles)
        for i, particle in enumerate(particles):
            particle.update_velocity(accelerations[i], dt)

        for particle in particles:
            particle.update_position(dt)

        if step != 0 and step % (steps // 100) == 0:
            print(f"{(step / steps) * 100:.1f}%")
