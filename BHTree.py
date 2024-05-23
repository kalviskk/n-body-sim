import numpy as np
from numba import njit
from collections import deque


@njit
def calculate_force_numba(
    body_position, body_mass, bodies_positions, bodies_masses, G=0.01
):
    force = np.zeros(2)
    for i in range(len(bodies_positions)):
        r_ij = bodies_positions[i] - body_position
        distance = np.linalg.norm(r_ij)
        if distance > 0:  # Avoid division by zero
            force += G * body_mass * bodies_masses[i] * r_ij / distance**3
    return force


class BHTree:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.center_of_mass = np.zeros(2)
        self.total_mass = 0
        self.body = None
        self.quadrants = [None, None, None, None]  # NW, NE, SW, SE

    def insert(self, body):
        if self.body is None and all(q is None for q in self.quadrants):
            self.body = body
            self.center_of_mass = body.position
            self.total_mass = body.mass
        else:
            if self.body is not None:
                self.subdivide()
                self.insert_body_into_quadrant(self.body)
                self.body = None
            self.insert_body_into_quadrant(body)

            self.total_mass += body.mass
            self.center_of_mass = (
                (self.center_of_mass * (self.total_mass - body.mass))
                + body.position * body.mass
            ) / self.total_mass

    def insert_body_into_quadrant(self, body):
        quadrant_index = self.get_quadrant_index(body.position)
        if self.quadrants[quadrant_index] is None:
            x_mid = (self.x_min + self.x_max) / 2
            y_mid = (self.y_min + self.y_max) / 2
            if quadrant_index == 0:
                self.quadrants[0] = BHTree(self.x_min, x_mid, y_mid, self.y_max)
            elif quadrant_index == 1:
                self.quadrants[1] = BHTree(x_mid, self.x_max, y_mid, self.y_max)
            elif quadrant_index == 2:
                self.quadrants[2] = BHTree(self.x_min, x_mid, self.y_min, y_mid)
            elif quadrant_index == 3:
                self.quadrants[3] = BHTree(x_mid, self.x_max, self.y_min, y_mid)
        self.quadrants[quadrant_index].insert(body)

    def subdivide(self):
        x_mid = (self.x_min + self.x_max) / 2
        y_mid = (self.y_min + self.y_max) / 2
        self.quadrants[0] = BHTree(self.x_min, x_mid, y_mid, self.y_max)
        self.quadrants[1] = BHTree(x_mid, self.x_max, y_mid, self.y_max)
        self.quadrants[2] = BHTree(self.x_min, x_mid, self.y_min, y_mid)
        self.quadrants[3] = BHTree(x_mid, self.x_max, self.y_min, y_mid)

    def get_quadrant_index(self, position):
        x, y = position
        x_mid = (self.x_min + self.x_max) / 2
        y_mid = (self.y_min + self.y_max) / 2
        if x < x_mid and y >= y_mid:
            return 0
        elif x >= x_mid and y >= y_mid:
            return 1
        elif x < x_mid and y < y_mid:
            return 2
        else:
            return 3

    def calculate_force(self, body, theta=1.5, G=0.01):
        force = np.zeros(2)
        stack = deque([self])

        while stack:
            node = stack.pop()
            if node.body is not None and node.body is not body:
                r_ij = node.body.position - body.position
                distance = np.linalg.norm(r_ij)
                if distance > 0:  # Avoid division by zero
                    force += G * body.mass * node.body.mass * r_ij / distance**3
            elif any(q is not None for q in node.quadrants):
                s = node.x_max - node.x_min
                d = np.linalg.norm(node.center_of_mass - body.position)
                if s / d < theta:
                    if d > 0:  # Avoid division by zero
                        r_ij = node.center_of_mass - body.position
                        force += G * body.mass * node.total_mass * r_ij / d**3
                else:
                    for quadrant in node.quadrants:
                        if quadrant is not None:
                            stack.append(quadrant)

        return force

    def calculate_all_forces(self, particles, G=0.01, theta=0.5):
        positions = np.array([p.position for p in particles])
        masses = np.array([p.mass for p in particles])
        forces = np.zeros((len(particles), 2))

        for i, body in enumerate(particles):
            forces[i] = calculate_force_numba(
                body.position, body.mass, positions, masses, G
            )

        return forces

    def plot(self, ax):
        # Plotting the rectangular regions
        ax.plot(
            [self.x_min, self.x_min, self.x_max, self.x_max, self.x_min],
            [self.y_min, self.y_max, self.y_max, self.y_min, self.y_min],
            "g-",
            linewidth=1,
        )
        # Adding a body to ax
        if self.body is not None:
            ax.scatter(self.body.position[0], self.body.position[1], color="white", s=3)

        ax.set_facecolor("black")  # Black background

        # Plotting the quadrants
        for quadrant in self.quadrants:
            if quadrant is not None:
                quadrant.plot(ax)
