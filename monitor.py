import math
import time
from multiprocessing import Manager, Process

import computation
import utils
import tsp

SLEEP_INTERVAL = 0.5


def recorder(f, states, start_state, iterations):
    memory = Manager().dict()
    memory['cost'] = 0

    process = Process(target=f, args=(states, start_state, iterations, memory))
    process.start()

    time.sleep(SLEEP_INTERVAL)

    costs = []
    while process.is_alive():
        costs.append(memory['cost'])
        time.sleep(SLEEP_INTERVAL)

    return costs


def myopic_monitor(f, states, start_state, profile_1, profile_3, config):
    time_class = 0

    memory = Manager().dict()
    memory['cost'] = 0

    process = Process(target=f, args=(states, start_state, 1000, memory))
    process.start()

    time.sleep(SLEEP_INTERVAL)

    heuristic_cost = tsp.get_mst_distance(start_state, states)

    while process.is_alive():
        quality_estimate = heuristic_cost / memory['cost']

        mevc = computation.get_mevc(quality_estimate, time_class, profile_1, profile_3, config)
        print("MEVC = %f" % mevc)
        if mevc <= 0:
            process.terminate()
            print("Final Quality = %f" % quality_estimate)
            break

        time_class += 1
        time.sleep(SLEEP_INTERVAL)
