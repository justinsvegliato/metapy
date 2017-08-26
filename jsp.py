import numpy as np
import random
import matplotlib.pyplot as plt
import copy

GENERATIONS = 500
POPULATION_SIZE = 500
ELITE_PROPORTION = 0.05
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.1


def get_location(assignment, job_id):
    for machine_id, job_ids in enumerate(assignment):
        if job_id in job_ids:
            return machine_id, job_ids.index(job_id)


# def InitPopulation(ps, I):
#     """Generate initial population from random shuffles of the tasks."""
#     gene = [j for j in the number of jobs for t in I[j]]
#     population = []
#     for i in xrange(ps):
#         shuffle(gene)
#         population.append([j for j in gene])
#     return population


def load_instance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

        jobs = []
        for line in lines[3:]:
            entries = [int(entry) for entry in line.strip().split(' ')]
            jobs.append([{'machine_id': entries[i], 'duration': entries[i + 1]} for i in range(0, len(entries), 2)])

        return {
            'num_machines': int(lines[0]),
            'num_jobs': int(lines[1]),
            'job_size': int(lines[2]),
            'jobs': jobs
        }


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


def get_crossed_assignment(p1, p2, I):
    def Index(p1, I):
        ct = [0 for j in xrange(I.n)]
        s = []
        for i in p1:
            s.append((i, ct[i]))
            ct[i] = ct[i] + 1
        return s

    idx_p1 = Index(p1, I)
    idx_p2 = Index(p2, I)
    nt = len(idx_p1) # total number of tasks
    i = randint(1, nt)
    j = randint(0, nt-1)
    k = randint(0, nt)
    implant = idx_p1[j:min(j+i,nt)] + idx_p1[:i - min(j+i,nt) + j]

    lft_child = idx_p2[:k]
    rgt_child = idx_p2[k:]
    for jt in implant:
        if jt in lft_child: lft_child.remove(jt)
        if jt in rgt_child: rgt_child.remove(jt)

    child = [ job for (job, task) in lft_child + implant + rgt_child ]
    return child


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
    # num_machines = 5
    # num_jobs = 50

    # costs = get_random_costs(num_machines, num_jobs)

    # generations = 400
    # population_size = 1000
    # elite_population_size = int(0.9 * population_size)

    # qualities = []

    # population = [get_random_assignment(num_machines, num_jobs) for i in range(population_size)]

    # for generation in range(generations):
    #     new_population = get_elite_population(population, costs, elite_population_size)
    #     new_population = [get_mutated_assignment(assignment, num_machines, num_jobs) for assignment in new_population]

    #     sorted_population = get_sorted_population(population, costs)
    #     sorted_population[-elite_population_size:] = new_population

    #     population = sorted_population

    #     quality = 1.5 / get_total_cost(population[0], costs)
    #     qualities.append(quality)

    #     print(generation, quality)

    # with open('q.txt') as f:
    #     qualities = [5000 / float(quality) for quality in f.readlines()]

    # plt.figure()
    # plt.title('Performance Profile')
    # plt.xlabel('Time')
    # plt.ylabel('Costs')
    # plt.scatter(range(len(qualities)), qualities)
    # plt.show()

    print(load_instance('q.txt'))


if __name__ == '__main__':
    main()
