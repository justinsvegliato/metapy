import itertools
import random
import re

import numpy as np


def load_instance(filename):
    with open(filename) as f:
        lines = f.readlines()

        size = int(lines[0])

        weights = ''
        for i in range(2, size + 2):
            weights += lines[i].strip()
            if i < size + 1:
                weights += ';'

        distances = ''
        for i in range(size + 3, 2 * size + 3):
            distances += lines[i].strip()
            if i < 2 * size + 2:
                distances += ';'

        return size, np.matrix(weights), np.matrix(distances)


def generate_instance(size):
    np.set_printoptions(threshold=np.nan)

    weights = np.random.random_integers(0, 10, size=(size, size))
    weight_matrix = weights + weights.T
    np.fill_diagonal(weight_matrix, 0)

    distances = np.random.random_integers(0, 10, size=(size, size))
    distance_matrix = distances + distances.T
    np.fill_diagonal(distance_matrix, 0)

    return size, weight_matrix, distance_matrix


def save_instance(filename, size, weight_matrix, distance_matrix):
    instance = str(size)

    weight_matrix_string = re.sub(r'[\[\]]', '', np.array_str(weight_matrix, max_line_width=10000))
    distance_matrix_string = re.sub(r'[\[\]]', '', np.array_str(distance_matrix, max_line_width=10000))

    instance += '\n\n' + weight_matrix_string + '\n\n' + distance_matrix_string

    f = open(filename, 'w')
    f.write(instance)
    f.close()


def get_random_matrix(rows, columns):
    return np.random.rand(rows, columns)


def get_random_assignment(size):
    return np.random.choice(range(size), size=size, replace=False)


def get_next_assignment(assignment):
    choices = range(len(assignment))
    first_variable, second_variable = np.random.choice(choices, size=2, replace=False)

    next_assignment = list(assignment)
    next_assignment[first_variable], next_assignment[second_variable] = next_assignment[second_variable], next_assignment[first_variable]

    return next_assignment


def get_cost(assignment, weights, distances): 
    pairs = itertools.permutations(range(len(assignment)), 2)
    return np.sum([weights[loc_1, loc_2] * distances[assignment[loc_1], assignment[loc_2]] for loc_1, loc_2 in pairs])


def anytime_simulated_annealing(size, weights, distances, memory, temperature=1, cooling_rate=0.0001):
    assignment = get_random_assignment(size)

    best_assignment = assignment 
    best_assignments = [best_assignment]

    while temperature > 0:
        next_assignment = get_next_assignment(assignment)

        cost = get_cost(assignment, weights, distances)
        next_cost = get_cost(next_assignment, weights, distances)

        energy_change = cost - next_cost

        if min(1, np.exp(energy_change / temperature)) >= random.random():
            assignment = next_assignment

            best_cost = get_cost(best_assignment, weights, distances)
            if best_cost > next_cost:
                best_assignment = next_assignment

            best_assignments.append(best_assignment)

            memory["solution"] = best_assignment
            memory["cost"] = get_cost(best_assignment, weights, distances)

        temperature -= cooling_rate
            
    return best_assignments
