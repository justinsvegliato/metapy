import itertools
import operator
import math
import random
import time
from multiprocessing import Manager, Process

import matplotlib.pyplot as plt
import numpy as np

import computation
import tsp
import utils

SLEEP_INTERVAL = 0.5


def k_opt_solve(states, start_state, iterations, memory):
    tour = tsp.get_initial_random_tour(states, start_state)
    cities = tsp.get_swappable_cities(tour)
    distance = tsp.get_tour_distance(tour)

    for t in range(iterations):
        has_changed = False

        best_tour = tour
        best_distance = distance
        for first_key, second_key in itertools.combinations(cities, 2):
            current_tour = tsp.get_mutated_tour(tour, first_key, second_key)
            current_distance = tsp.get_tour_distance(current_tour)

            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance

                has_changed = True

        tour = best_tour
        distance = best_distance

        memory['cost'] = distance
        memory['time'] = time.time()

        if not has_changed:
            break

    return tour


def recorder(f):    
    start_time = time.time()

    memory = Manager().dict()
    memory['cost'] = 0
    memory['time'] = start_time

    process = Process(target=f, args=(states, start_state, 1000, memory))
    process.start()

    time.sleep(SLEEP_INTERVAL)

    performance = []
    while process.is_alive():
        
        performance.append((time, quality))
        time.sleep(SLEEP_INTERVAL)

    return performance


def myopic_monitor(f, profile_1, profile_3, config):
    start_cost = 0
    start_time = time.time()
    heuristic = 0

    memory = Manager().dict()
    memory['cost'] = start_cost
    memory['time'] = start_time

    process = Process(target=f, args=(states, start_state, 1000, memory))
    process.start()

    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality_class = utils.digitize(heuristic / memory['cost'], config['solution_quality_class_bounds'])
        time_class = math.floor((memory['time'] - start_time) / SLEEP_INTERVAL)

        mevc = computation.get_mevc(quality_class, time_class, profile_1, profile_3, config)
        if mevc <= 0:
            process.terminate()
            break

        time.sleep(SLEEP_INTERVAL)


def main():


# def main():
#     TIME_COST_MULTIPLIER = 0.1
#     INTRINSIC_VALUE_MULTIPLIER = 200
#     SOLUTION_QUALITY_CLASS_COUNT = 20
#     SOLUTION_QUALITY_CLASS_BOUNDS = np.linspace(0, 1, SOLUTION_QUALITY_CLASS_COUNT + 1)
#     SOLUTION_QUALITY_CLASSES = range(SOLUTION_QUALITY_CLASS_COUNT)

#     config = {
#         'intrinsic_value_multiplier': INTRINSIC_VALUE_MULTIPLIER,
#         'time_cost_multiplier': TIME_COST_MULTIPLIER,
#         'solution_quality_class_count': SOLUTION_QUALITY_CLASS_COUNT,
#         'solution_quality_class_bounds': SOLUTION_QUALITY_CLASS_BOUNDS,
#         'solution_quality_classes': SOLUTION_QUALITY_CLASSES
#     }

#     profile_1 = performance.get_dynamic_performance_profile(instances, CONFIG, performance.TYPE_1)
#     profile_3 = performance.get_dynamic_performance_profile(instances, CONFIG, performance.TYPE_3)

#     myopic_monitor(k_opt_solve, profile_1, profile_3, config)


if __name__ == "__main__":
    main()
