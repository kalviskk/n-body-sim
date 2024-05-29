from Particle import Particle
import numpy as np
import matplotlib as plt
import cmocean


def createParticles(
    N, height, width, G, ring_radius=600, central_mass=1, distribution="ring"
):
    particles = []
    particle_mass = 1  # Much smaller than the central mass
    particle_radius = 0.01
    central_mass = 10000
    center = np.array([height / 2, width / 2])

    if distribution == "ring":
        colormap = cmocean.cm.phase
        for _ in range(N):
            angle = np.random.rand() * 2 * np.pi
            radius = np.random.rand() * ring_radius + 5 * ring_radius * 0.1
            position = center + np.array([np.cos(angle), np.sin(angle)]) * radius

            # Calculate velocity for a circular orbit
            c_distance = np.linalg.norm(position - center)
            v_var = (np.random.rand() * 0.2) - 0.2  # velocity variation
            orbital_velocity = np.sqrt(G * central_mass / c_distance) * (1 + v_var)
            velocity_direction = np.array(
                [-np.sin(angle), np.cos(angle)]
            )  # Perpendicular to radius
            velocity = (
                velocity_direction * orbital_velocity
            )  # Reduce velocity to keep particles bound

            # Determine the color based on the normalized angle
            normalized_angle = angle / (2 * np.pi)
            color = colormap(normalized_angle)
            particles.append(
                Particle(position, velocity, particle_mass, particle_radius, color)
            )

        # Adding the central massive object
        particles.append(
            Particle(center, np.array([0, 0]), central_mass, 0.01, "white")
        )

        return particles
    if distribution == "uniform":
        colormap_x = cmocean.tools.crop_by_percent(
            cmocean.cm.matter, 30, which="max", N=None
        )
        for _ in range(N):
            position = np.random.rand(2) * np.array([width, height])
            velocity = np.array([0, 0])

            # Determine the colors based on normalized positions
            normalized_x = position[0] / width
            normalized_y = position[1] / height

            # Blend the colors from the two colormaps
            color_x = np.array(colormap_x(normalized_x))
            # color_y = np.array(colormap_y(normalized_y))
            color = color_x

            particles.append(
                Particle(position, velocity, particle_mass, particle_radius, color)
            )

        return particles

    if distribution == "two":
        pos_S = center
        pos_e = np.array([width, height / 2])

        mass_S = 10000
        mass_e = 1
        distance = np.linalg.norm(pos_S - pos_e)
        velocity_e = np.sqrt(G * mass_S / distance) * 0.8

        particles = [
            Particle(pos_S, np.array([0, 0]), mass_S, 0.1, "ivory"),
            Particle(pos_e, np.array([0, 1]) * velocity_e, mass_e, 0.1, "green"),
        ]
        return particles

    if distribution == "three":
        particle_mass = 100
        pos_A = np.random.rand(2) * np.array([width, height])
        pos_B = np.random.rand(2) * np.array([width, height])
        pos_C = np.random.rand(2) * np.array([width, height])

        # Initial velocities to achieve a figure-8 shape
        vel_A = np.random.rand(2) * 0
        vel_B = np.random.rand(2) * 0
        vel_C = np.random.rand(2) * 0

        particles = [
            Particle(pos_A, vel_A, particle_mass, particle_radius, "red"),
            Particle(pos_B, vel_B, particle_mass, particle_radius, "blue"),
            Particle(pos_C, vel_C, particle_mass, particle_radius, "green"),
        ]

        return particles
