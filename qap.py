import numpy as np
import random
import matplotlib.pyplot as plt


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
    return np.sum([weights[variable][value] * distances[variable][value] for variable, value in enumerate(assignment)])


def anytime_simulated_annealing(size, weights, distances, temperature=1, cooling_rate=0.0001):
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

        temperature -= cooling_rate
            
    return best_assignments


def main():
    size = 1000

    weights = get_random_matrix(size, size)
    distances = get_random_matrix(size, size)

    best_assignments = anytime_simulated_annealing(size, weights, distances)
    qualities = [get_cost(assignment, weights, distances) for assignment in best_assignments]

    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('Solution Quality')
    plt.plot(range(len(best_assignments)), qualities)
    plt.show()


if __name__ == '__main__':
    main()


