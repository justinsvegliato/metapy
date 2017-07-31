import json
import math
import time
from multiprocessing import Manager, Process

from scipy.optimize import curve_fit

import computation
import tsp
import utils
import numpy as np

SLEEP_INTERVAL = 0.5


def recorder(algorithm, *args):
    memory = Manager().dict()
    memory["cost"] = None
    args += (memory,)

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    costs = []
    while process.is_alive():
        costs.append(memory["cost"])
        time.sleep(SLEEP_INTERVAL)

    return costs


def fixed_monitor(algorithm, quality_estimator, profile_4, config, *args):
    memory = Manager().dict()
    memory["solution"] = None
    memory["cost"] = None
    args += (memory,)

    step = 0
    stopping_point = computation.get_fixed_stopping_point(profile_4, config)
    records = []

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory["cost"])

        record = {"t": step, "q": quality}
        records.append(record)

        print(record)

        if step == stopping_point:
            process.terminate()
            break

        step += 1
        time.sleep(SLEEP_INTERVAL)

    return memory["solution"], records


def myopic_monitor(algorithm, quality_estimator, profile_1, profile_3, config, *args):
    memory = Manager().dict()
    memory["solution"] = None
    memory["cost"] = None
    args += (memory,)

    step = 0
    records = []

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory["cost"])

        record = {"t": step, "q": quality}
        records.append(record)

        print(record)

        mevc = computation.get_mevc(quality, step, profile_1, profile_3, config)
        if mevc <= 0:
            process.terminate()
            break

        step += 1
        time.sleep(SLEEP_INTERVAL)

    return memory["solution"], records


def nonmyopic_monitor(algorithm, quality_estimator, profile_2, profile_3, config, *args):
    memory = Manager().dict()
    memory["solution"] = None
    memory["cost"] = 0
    args += (memory,)

    values = computation.get_optimal_values(profile_2, profile_3, config)
    step = 0
    records = []

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory["cost"])

        record = {"t": step, "q": quality}
        records.append(record)

        print(record)

        action = computation.get_optimal_action(quality, step, values, profile_2, profile_3, config)
        if action == computation.STOP_SYMBOL:
            process.terminate()
            break

        step += 1
        time.sleep(SLEEP_INTERVAL)

    return memory["solution"], records

def projected_monitor(algorithm, quality_estimator, config, *args):
    memory = Manager().dict()
    memory["solution"] = None
    memory["cost"] = 0
    args += (memory,)

    model = lambda x, a, b, c: a * np.arctan(x + b) + c
    step = 0
    history = []
    records = []

    process = Process(target=algorithm, args=args)
    process.start()
    time.sleep(SLEEP_INTERVAL)

    while process.is_alive():
        quality = quality_estimator(memory["cost"])
        history.append(quality)

        record = {"t": step, "q": quality}
        records.append(record)

        print(record)

        if step >= 10:
            try:
                steps = range(len(history))
                params, _ = curve_fit(model, steps, history)
                projection = model(range(32), params[0], params[1], params[2])

                comprehensive_values = computation.get_time_dependent_utility(projection, range(32), config['intrinsic_value_multiplier'], config['time_cost_multiplier'])
                stopping_point = computation.get_optimal_stopping_point(comprehensive_values)

                if stopping_point <= step:
                    process.terminate()
                    break
            except (RuntimeError, TypeError):
                pass

        step += 1
        time.sleep(SLEEP_INTERVAL)

    return memory["solution"], records
