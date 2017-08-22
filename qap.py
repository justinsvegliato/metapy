import numpy as np
import random
import matplotlib.pyplot as plt


def get_random_matrix(size):
    return np.random.rand(size, size)


def get_random_assignment(size):
    return np.random.choice(range(size), size=size, replace=False)


def get_next_assignment(assignment):
    mutated_assignment = list(assignment)
    first_location, second_location = np.random.choice(range(len(assignment)), size=2, replace=False)
    mutated_assignment[first_location], mutated_assignment[second_location] = mutated_assignment[second_location], mutated_assignment[first_location]
    return mutated_assignment


def get_cost(weights, distances, location_id, facility_id):
    return weights[location_id][facility_id] * distances[location_id][facility_id]


def get_total_cost(assignment, weights, distances):
    return np.sum([get_cost(weights, distances, location_id, facility_id) for location_id, facility_id in enumerate(assignment)])


def simulated_annealing(size, weights, distances):
    assignment = get_random_assignment(size)
    best_assignment = assignment    
    temperature = 1
    assignments = []

    while temperature > 0:
        next_assignment = get_next_assignment(assignment)

        cost = get_total_cost(assignment, weights, distances)
        next_cost = get_total_cost(next_assignment, weights, distances)
        energy_change = cost - next_cost

        if min(1, np.exp(energy_change / temperature)) >= random.random():
        # if energy_change > 0 or np.exp(energy_change / temperature) >= random.random():
            assignment = next_assignment

            best_cost = get_total_cost(best_assignment, weights, distances)
            assignments.append(best_assignment)
            if best_cost > next_cost:
                best_assignment = next_assignment
        temperature -= 0.0001
            
    return assignments


# size = 1000
# size = 10000
weights = np.ones((size, size)) #get_random_matrix(size)
distances = get_random_matrix(size)

assignments = simulated_annealing(size, weights, distances)
qualities = [1 / get_total_cost(assignment, weights, distances) for assignment in assignments]

plt.figure()
plt.xlabel('Time')
plt.ylabel('Cost')
plt.plot(range(len(assignments)), qualities)
plt.show()


