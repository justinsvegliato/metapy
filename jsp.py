import numpy as np
import random
import matplotlib.pyplot as plt


def get_random_matrix(size):
    return np.random.rand(size, size)


def get_random_assignment(num_machines, num_jobs):
    return 


def get_next_assignment(assignment):
    mutated_assignment = list(assignment)
    first_location, second_location = np.random.choice(range(len(assignment)), size=2, replace=False)
    mutated_assignment[first_location], mutated_assignment[second_location] = mutated_assignment[second_location], mutated_assignment[first_location]
    return mutated_assignment


def get_cost(weights, distances, location_id, facility_id):
    return weights[location_id][facility_id] * distances[location_id][facility_id]


def get_total_cost(assignment, weights, distances):
    return np.sum([get_cost(weights, distances, location_id, facility_id) for location_id, facility_id in enumerate(assignment)])

