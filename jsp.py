import numpy as np
import random
import matplotlib.pyplot as plt
import copy


def get_location(assignment, job):
    for machine_id in range(len(assignment)):
        machine = assignment[machine_id]
        if job in machine:
            return machine_id, machine.index(job)


def get_random_costs(num_machines, num_jobs):
    return np.random.rand(num_machines, num_jobs)


def get_random_assignment(num_machines, num_jobs):
    machines = range(num_machines)
    jobs = range(num_jobs)

    assignment = [[] for _ in machines]

    for job_id in jobs:
        machine_id = random.choice(machines)
        assignment[machine_id].append(job_id)

    return assignment


def get_mutated_assignment(assignment, num_machines, num_jobs):
    machines = range(num_machines)
    jobs = range(num_jobs)

    new_assignment = copy.deepcopy(assignment)

    for i in range(10):
        while assignment == new_assignment:
            machine = random.choice(machines)
            job = random.choice(jobs)

            i, j = get_location(assignment, job)
            del new_assignment[i][j]

            new_assignment[machine].append(job)

    return new_assignment


def get_cost(costs, machine_id, job_id):
    return costs[machine_id, job_id]


def get_total_cost(assignment, costs):
    total_costs = []
    for machine_id in range(len(assignment)):
        machine = assignment[machine_id]

        cost = 0
        for job_id in machine:
            cost += get_cost(costs, machine_id, job_id)
        total_costs.append(cost)

    return np.max(total_costs)


min_speed = 1
max_speed = 10
num_machines = 10


min_length = 1
max_length = 10000
num_jobs = 500

assignment = get_random_assignment(num_machines, num_jobs)
costs = get_random_costs(num_machines, num_jobs)
mutated_assignment = get_mutated_assignment(assignment, num_machines, num_jobs)

for generation in range(1000):
    population = [get_random_assignment(num_machines, num_jobs) for i in range(100)]
    mutated_population = [get_mutated_assignment(assignment, num_machines, num_jobs) for assigment in population]
    sorted_population = sorted([(get_total_cost(mutated_assignment, costs), mutated_assignment) for mutated_assignment in mutated_population], key=lambda k: k[0])
    population = [thing[1] for thing in sorted_population[:5]]

    for _ in range(25):
        population.append(get_random_assignment(num_machines, num_jobs))

    # print(population[0])
    print(get_total_cost(population[0], costs))

