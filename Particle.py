import numpy as np


# kaut kas negāja ar dtype, tāpēc forcoju visiem float64
class Particle:
    def __init__(self, position, velocity, mass, radius, color):
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.mass = np.float64(mass)
        self.radius = np.float64(radius)
        self.color = color  # Add color attribute

    def update_velocity(self, acceleration, dt):
        acceleration = np.array(acceleration, dtype=np.float64)
        self.velocity += acceleration * np.float64(dt)

    def update_position(self, dt):
        self.position += self.velocity * np.float64(dt)
