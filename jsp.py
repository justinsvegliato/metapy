import numpy as np
import random
import matplotlib.pyplot as plt
import copy


def get_location(assignment, job_id):
    for machine_id, job_ids in enumerate(assignment):
        if job_id in job_ids:
            return machine_id, job_ids.index(job_id)


def get_random_assignment(num_machines, num_jobs):
    machine_ids = range(num_machines)
    job_ids = range(num_jobs)

    assignment = [[] for _ in machine_ids]

    for job_id in job_ids:
        machine_id = random.choice(machine_ids)
        assignment[machine_id].append(job_id)

    return assignment


def get_mutated_assignment(assignment, num_machines, num_jobs):
    machine_ids = range(num_machines)
    job_ids = range(num_jobs)

    new_assignment = copy.deepcopy(assignment)

    job_id = random.choice(job_ids)

    while assignment == new_assignment:
        new_machine_id = random.choice(machine_ids)
        new_assignment[new_machine_id].append(job_id)

        old_machine_id, slot = get_location(assignment, job_id)
        del new_assignment[old_machine_id][slot]

    return new_assignment


def get_random_costs(num_machines, num_jobs):
    return np.random.rand(num_machines, num_jobs)


def get_total_cost(assignment, costs):
    total_costs = []

    for machine_id, job_ids in enumerate(assignment):
        cost = 0
        for job_id in job_ids:
            cost += costs[machine_id, job_id]

        total_costs.append(cost)

    return np.max(total_costs)


def get_sorted_population(population, costs):
    sorted_pairs = sorted([(get_total_cost(assignment, costs), assignment) for assignment in population], key=lambda k: k[0])
    return [assignment for _, assignment in sorted_pairs]


def get_elite_population(population, costs, size):
    sorted_population = get_sorted_population(population, costs)
    return [assignment for assignment in sorted_population[:size]]


def main():
    num_machines = 5
    num_jobs = 50

    costs = get_random_costs(num_machines, num_jobs)
    # costs = np.matrix([[0.97188071, 0.05795095, 0.19207029, 0.3883632, 0.27602015, 0.4979248, 0.24620109, 0.73204223, 0.24851216, 0.66713638], 
    #                 [0.99284099, 0.54011251, 0.86960698, 0.40496969, 0.16749654, 0.58906524, 0.01747369, 0.89810728, 0.37468181, 0.86894554], 
    #                 [0.3420342, 0.34764302, 0.0380342, 0.64255261, 0.85022931, 0.08053618, 0.44643143, 0.94173863, 0.64872432, 0.05583479], 
    #                 [0.81696921, 0.82957557, 0.74362754, 0.0137083, 0.13724315, 0.49883214, 0.97145286, 0.33193399, 0.17220811, 0.48126264], 
    #                 [0.78329609, 0.43502877, 0.07277983, 0.55379149, 0.21066182, 0.63106304, 0.61506724, 0.29250189, 0.24160404, 0.67692696]])

    generations = 1000
    population_size = 1000
    elite_population_size = int(0.9 * population_size)

    qualities = []

    population = [get_random_assignment(num_machines, num_jobs) for i in range(population_size)]

    for generation in range(generations):
        new_population = get_elite_population(population, costs, elite_population_size)
        new_population = [get_mutated_assignment(assignment, num_machines, num_jobs) for assignment in new_population]

        sorted_population = get_sorted_population(population, costs)
        sorted_population[-elite_population_size:] = new_population

        population = sorted_population

        quality = 1.5 / get_total_cost(population[0], costs)
        qualities.append(quality)

        print(generation, quality)

    plt.figure()
    plt.title('Performance Profile')
    plt.xlabel('Time')
    plt.ylabel('Costs')
    plt.scatter(range(len(qualities)), qualities)
    plt.show()


if __name__ == '__main__':
    main()
