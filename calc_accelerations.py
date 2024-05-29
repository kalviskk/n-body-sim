import numpy as np
from Particle import Particle
from BHTree import tree_based_algorithm, calculate_force_for_tree


def calculate_accelerations(particles, theta=1.5):
    N = len(particles)
    accelerations = np.zeros((N, 2), dtype=np.float64)

    root = tree_based_algorithm(particles, theta)

    for i, particle in enumerate(particles):
        force = calculate_force_for_tree(root, particle.position, particle.mass)
        accelerations[i] = force / particle.mass

    return accelerations
