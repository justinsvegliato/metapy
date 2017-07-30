import math
import time
from multiprocessing import Manager, Process

import computation
import tsp
import utils
import json

SLEEP_INTERVAL = 0.5


def recorder(algorithm, *args):
    memory = Manager().dict()
    memory['cost'] = None
    args += (memory,)

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    costs = []
    while process.is_alive():
        costs.append(memory['cost'])
        time.sleep(SLEEP_INTERVAL)

    return costs


def fixed_monitor(algorithm, quality_estimator, profile_4, config, *args):
    memory = Manager().dict()
    memory['solution'] = None
    memory['cost'] = None
    args += (memory,)

    step = 0
    stopping_point = computation.get_fixed_stopping_point(profile_4, config)
    records = []
    
    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory['cost'])

        record = {"t": step, "q": quality}
        records.append(record)

        utils.log(record)

        if step == stopping_point:
            process.terminate()
            break

        step += 1
        time.sleep(SLEEP_INTERVAL)

    return memory['solution'], records


def myopic_monitor(algorithm, quality_estimator, profile_1, profile_3, config, *args):
    memory = Manager().dict()
    memory['solution'] = None    
    memory['cost'] = None
    args += (memory,)

    step = 0
    records = []

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory['cost'])
        
        record = {"t": step, "q": quality}
        records.append(record)

        utils.log(record)

        mevc = computation.get_mevc(quality, step, profile_1, profile_3, config)
        if mevc <= 0:
            process.terminate()
            break

        step += 1
        time.sleep(SLEEP_INTERVAL)

    return memory['solution'], records


def nonmyopic_monitor(algorithm, quality_estimator, profile_2, profile_3, config, *args):
    memory = Manager().dict()
    memory['solution'] = None        
    memory['cost'] = 0
    args += (memory,)

    values = computation.get_optimal_values(profile_2, profile_3, config)
    step = 0
    records = []

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory['cost'])

        record = {"t": step, "q": quality}
        records.append(record)

        utils.log(record)

        action = computation.get_optimal_action(quality, step, values, profile_2, profile_3, config)
        if action == computation.STOP_SYMBOL:
            process.terminate()
            break

        step += 1        
        time.sleep(SLEEP_INTERVAL)

    return memory['solution'], records
