import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import monitor
import itertools
import experiments
import os

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


def main():

    # model = lambda x, a, b, c: a * np.arctan(x + b) + c

    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('Solution Quality')

    source = 'problems/10-19-qap/'
    for filename in os.listdir(source):
        if filename.endswith(".dat"):
            file_path = os.path.join(source, filename)

            instance = os.path.splitext(filename)[0]
            bounds = experiments.get_optimal_costs('problems/lower-bounds.csv')

            size, weights, distances = load_instance(file_path)
            costs = monitor.recorder(anytime_simulated_annealing, size, weights, distances)

            qualities = [bounds[instance] / cost for cost in costs]
            plt.plot(range(len(qualities)), qualities)

    # steps = range(len(qualities))

    # axes = plt.gca()
    # axes.set_ylim([0, 1])

    # for end in steps[5:]:
    #     try:
    #         params, _ = curve_fit(model, steps[:end], qualities[:end])
    #         projection = model(steps, params[0], params[1], params[2])
    #         plt.plot(steps, projection)
    #     except:
    #         pass

    plt.show()


if __name__ == '__main__':
    main()

