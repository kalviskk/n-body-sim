# This is taken from https://github.com/Gongure/n-body-simulation-methods/blob/main/treebasedalgorithm.py
# I had difficulties creating my own implementation of the Barnes-Hut algorithm
# so I edited Gongure's code to work for my program, but all credit goes to the creator
# https://github.com/Gongure/n-body-simulation-methods/commits?author=Gongure

import copy
import numpy as np
from Particle import Particle

G = 1  # Gravitational constant


# Create a class for nodes in the tree
class Node:
    def __init__(self):
        self.children = None  # Children nodes
        self.mass = None  # Total mass of the node
        self.center_of_mass = None  # Center of mass of the node
        self.bbox = None  # Bounding box of the node


# Main function to build the Barnes-Hut tree
def tree_based_algorithm(particles, input_theta):
    global theta
    theta = input_theta  # Threshold for node approximation

    # Create the root node
    root = Node()
    root.bbox = find_root_bbox([body.position for body in particles])

    global current_boxes
    current_boxes = [root.bbox]

    # Insert each particle into the tree
    for body in particles:
        m = copy.deepcopy(body.mass)
        p = copy.deepcopy(body.position)
        insert_in_tree(root, p, m)

    return root


# Recursive function to insert a particle into the tree
def insert_in_tree(node, body_position, body_mass):
    global current_boxes
    if node.mass is None:
        # If the node is empty, insert the particle here
        node.mass = copy.deepcopy(body_mass)
        node.center_of_mass = copy.deepcopy(body_position)
        return

    elif node.children is not None:
        # If the node is internal, update the center of mass and total mass,
        # then insert the particle in the appropriate quadrant
        node.center_of_mass = copy.deepcopy(
            (node.center_of_mass * node.mass + body_position * body_mass)
            / (node.mass + body_mass)
        )
        node.mass += copy.deepcopy(body_mass)
        quadrant = get_quadrant(node.bbox, copy.deepcopy(body_position))
        if node.children[quadrant] is None:
            node.children[quadrant] = Node()
            node.children[quadrant].bbox = find_bbox(node.bbox, quadrant)
            current_boxes.append(node.children[quadrant].bbox)
        insert_in_tree(
            node.children[quadrant],
            copy.deepcopy(body_position),
            copy.deepcopy(body_mass),
        )
        return

    elif node.children is None:
        # If the node is external, create children and redistribute the particle
        node.children = [None, None, None, None]

        old_quadrant = get_quadrant(node.bbox, node.center_of_mass)
        new_quadrant = get_quadrant(node.bbox, body_position)

        node.children[old_quadrant] = Node()
        node.children[old_quadrant].bbox = find_bbox(node.bbox, old_quadrant)
        current_boxes.append(node.children[old_quadrant].bbox)

        if new_quadrant != old_quadrant:
            node.children[new_quadrant] = Node()
            node.children[new_quadrant].bbox = find_bbox(node.bbox, new_quadrant)
            current_boxes.append(node.children[new_quadrant].bbox)

        insert_in_tree(
            node.children[old_quadrant],
            copy.deepcopy(node.center_of_mass),
            copy.deepcopy(node.mass),
        )
        insert_in_tree(
            node.children[new_quadrant],
            copy.deepcopy(body_position),
            copy.deepcopy(body_mass),
        )

        node.center_of_mass = copy.deepcopy(
            (node.center_of_mass * node.mass + body_position * body_mass)
            / (node.mass + body_mass)
        )
        node.mass += copy.deepcopy(body_mass)
        return


# Recursive function to calculate the force on a particle from the tree
def calculate_force_for_tree(node, body_position, mass):
    if node.mass == mass:
        # Ignore self-interaction
        return np.zeros(2, dtype=np.float64)

    elif node.children is None:
        # If the node is external, calculate the force directly
        resulting_force = calculate_gravity(
            node.center_of_mass, body_position, node.mass, mass
        )
        return resulting_force

    else:
        # If the node is internal, decide whether to use the node or its children
        s = np.linalg.norm(node.bbox[1][0] - node.bbox[0][0])
        d = np.linalg.norm(body_position - node.center_of_mass)
        if s / d < theta:
            resulting_force = calculate_gravity(
                node.center_of_mass, body_position, node.mass, mass
            )
            return resulting_force
        else:
            resulting_force = np.zeros(2, dtype=np.float64)
            for child in node.children:
                if child is not None:
                    resulting_force += calculate_force_for_tree(
                        child, body_position, mass
                    )
            return resulting_force


########################## Helper functions ##########################


# Calculate the gravitational force between two bodies
def calculate_gravity(other_body_position, body_position, other_body_mass, body_mass):
    connection_vector = other_body_position - body_position
    distance = np.linalg.norm(connection_vector)
    direction = connection_vector / distance
    force = G * (body_mass * other_body_mass) / (distance**2)
    resulting_force = force * direction
    return resulting_force


# Find the bounding box that contains all particles
def find_root_bbox(array_of_positions):
    min_x = min(array_of_positions, key=lambda x: x[0])[0]
    max_x = max(array_of_positions, key=lambda x: x[0])[0]
    min_y = min(array_of_positions, key=lambda x: x[1])[1]
    max_y = max(array_of_positions, key=lambda x: x[1])[1]
    max_diff = max(max_x - min_x, max_y - min_y)
    center = np.array([min_x, min_y]) + np.array([max_x - min_x, max_y - min_y]) / 2
    cmin = center - np.array([max_diff, max_diff]) / 2
    cmax = center + np.array([max_diff, max_diff]) / 2
    return [cmin, cmax]


# Determine the quadrant of a position within a bounding box
def get_quadrant(bbox, position):
    cmin = bbox[0]
    cmax = bbox[1]
    a = 0
    s = cmax[0] - cmin[0]
    if position[0] > s / 2 + cmin[0]:
        a = 1
    if position[1] > s / 2 + cmin[1]:
        a += 2
    return a


# Find the bounding box for a specific quadrant within a larger bounding box
def find_bbox(bbox, quadrant):
    cmin = bbox[0]
    cmax = bbox[1]
    x = (cmax[0] - cmin[0]) / 2
    y = (cmax[1] - cmin[1]) / 2
    center = cmin + np.array([x, y])
    if quadrant == 0:
        return [cmin, center]
    elif quadrant == 1:
        return [np.array([center[0], cmin[1]]), np.array([cmax[0], center[1]])]
    elif quadrant == 2:
        return [np.array([cmin[0], center[1]]), np.array([center[0], cmax[1]])]
    elif quadrant == 3:
        return [center, cmax]
