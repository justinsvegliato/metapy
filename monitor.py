import math
import time
from multiprocessing import Manager, Process

import computation
import utils

SLEEP_INTERVAL = 0.5


def recorder(f, states, start_state, iterations):    
    start_time = time.time()

    memory = Manager().dict()
    memory['cost'] = 0
    memory['time'] = time.time()

    process = Process(target=f, args=(states, start_state, iterations, memory))
    process.start()
    time.sleep(SLEEP_INTERVAL)

    checkpoints = []
    while process.is_alive():
        time_class = math.ceil((memory['time'] - start_time) / SLEEP_INTERVAL)
        checkpoint = time_class, memory['cost']
        checkpoints.append(checkpoint)
        time.sleep(SLEEP_INTERVAL)

    return checkpoints


def myopic_monitor(f, profile_1, profile_3, config):
    start_cost = 0
    start_time = time.time()

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


if __name__ == "__main__":
    main()
