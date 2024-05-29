# this is taken from https://github.com/Gongure/n-body-simulation-methods/blob/main/treebasedalgorithm.py
# I had difficulties to create my own implementation of barnes-hut algorithm
# so I edited Gongures code to work for my program, but all credit goes to the creator https://github.com/Gongure/n-body-simulation-methods/commits?author=Gongure
import copy
import numpy as np
from Particle import Particle

G = 1


# Create a class for nodes in the tree
class Node:
    def __init__(self):
        self.children = None
        self.mass = None
        self.center_of_mass = None
        self.bbox = None


def tree_based_algorithm(particles, input_theta):
    global theta
    theta = input_theta

    root = Node()
    root.bbox = find_root_bbox([body.position for body in particles])

    global current_boxes
    current_boxes = [root.bbox]

    for body in particles:
        m = copy.deepcopy(body.mass)
        p = copy.deepcopy(body.position)
        insert_in_tree(root, p, m)

    return root


def insert_in_tree(node, body_position, body_mass):
    global current_boxes
    if node.mass is None:
        node.mass = copy.deepcopy(body_mass)
        node.center_of_mass = copy.deepcopy(body_position)
        return

    elif node.children is not None:
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


def calculate_force_for_tree(node, body_position, mass):
    if node.mass == mass:
        return np.zeros(2, dtype=np.float64)

    elif node.children is None:
        resulting_force = calculate_gravity(
            node.center_of_mass, body_position, node.mass, mass
        )
        return resulting_force

    else:
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


def calculate_gravity(other_body_position, body_position, other_body_mass, body_mass):
    connection_vector = other_body_position - body_position
    distance = np.linalg.norm(connection_vector)
    direction = connection_vector / distance
    force = G * (body_mass * other_body_mass) / (distance**2)
    resulting_force = force * direction
    return resulting_force


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
