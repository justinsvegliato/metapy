import numpy as np
import random
import matplotlib.pyplot as plt
import copy

GENERATIONS = 500
POPULATION_SIZE = 5
ELITE_PROPORTION = 0.05
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.1


def generate_instance(num_machines, num_jobs, num_operations):
    instance = str(num_machines) + ' ' + str(num_jobs) + '\n'

    for i in range(num_jobs):
        job = str(num_operations) + ' '
        for _ in range(num_operations):
            job += str(random.choice(range(num_machines))) + ' ' + str(random.randint(1, 100)) + ' '

        instance += job + '\n'

    return instance


def get_lower_bound(instance):
    total_durations = []
    for job in instance['jobs']:
        total_duration = 0
        for operation in job:
            total_duration += operation['duration']
        total_durations.append(total_duration)
    return max(total_durations)


def load_instance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        num_machines, num_jobs = [int(item) for item in lines[0].split(' ')]

        jobs = []
        for line in lines[1:]:
            entries = [int(entry) for entry in line.strip().split(' ')]
            jobs.append([{'machine_id': entries[i], 'duration': entries[i + 1]} for i in range(1, len(entries), 2)])

        return {'num_machines': num_machines, 'num_jobs': num_jobs, 'jobs': jobs}


def get_random_assignment(instance):
    assignment = [machine_id for machine_id in range(instance['num_jobs']) for task in range(instance['num_operations'])]
    return random.sample(assignment, len(assignment))


def get_initial_population(population_size, instance):
    return [get_random_assignment(instance) for _ in range(population_size)]


def get_mutated_assignment(assignment):
    new_assignment = list(assignment)
    index1, index2 = np.random.choice(range(len(new_assignment)), 2, replace=False)
    new_assignment[index1], new_assignment[index2] = new_assignment[index2], new_assignment[index1]
    return new_assignment
