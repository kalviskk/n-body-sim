from pyqtree import Index
import numpy as np
from Particle import Particle


def calculate_accelerations(particles, G, theta=3, collision_radius=0.01):
    N = len(particles)
    accelerations = np.zeros((N, 2))

    # Determine the bounding box for the quadtree
    positions = np.array([p.position for p in particles])
    x_min, y_min = positions.min(axis=0)
    x_max, y_max = positions.max(axis=0)

    # Create the quadtree instance
    quadtree = Index(bbox=(x_min, y_min, x_max, y_max))

    # Insert particles into the quadtree
    for i, particle in enumerate(particles):
        quadtree.insert(
            item=i,
            bbox=(
                particle.position[0],
                particle.position[1],
                particle.position[0],
                particle.position[1],
            ),
        )

    # Calculate the force on each particle and compute the acceleration
    for i, particle in enumerate(particles):
        force = np.zeros(2)
        nearby_indices = quadtree.intersect(
            (
                particle.position[0] - theta,
                particle.position[1] - theta,
                particle.position[0] + theta,
                particle.position[1] + theta,
            )
        )

        for j in nearby_indices:
            if i != j:  # Avoid self-interaction
                other = particles[j]
                r_ij = other.position - particle.position
                distance = np.linalg.norm(r_ij)

                # if distance < other.radius + particle.radius:  # Handle collision
                #     # Calculate the new velocities using elastic collision equations
                #     v1 = particle.velocity
                #     v2 = other.velocity
                #     m1 = particle.mass
                #     m2 = other.mass

                #     v1_new = (
                #         v1
                #         - (2 * m2 / (m1 + m2))
                #         * np.dot(v1 - v2, r_ij)
                #         / np.dot(r_ij, r_ij)
                #         * r_ij
                #     )
                #     v2_new = v2 - (2 * m1 / (m1 + m2)) * np.dot(
                #         v2 - v1, -r_ij
                #     ) / np.dot(-r_ij, -r_ij) * (-r_ij)

                #     particle.velocity = v1_new
                #     other.velocity = v2_new

                # # Separation logic: Move particles apart
                # overlap = other.radius + particle.radius - distance
                # move_vector = r_ij / distance * overlap / 2
                # particle.position -= move_vector
                # other.position += move_vector
                if distance > 5 * (
                    other.radius + particle.radius
                ):  # Calculate gravitational force
                    force += G * particle.mass * other.mass * r_ij / distance**3

        accelerations[i] = force / particle.mass

    return accelerations
