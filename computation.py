import copy

import numpy as np

import utils

STOP_SYMBOL = 0
CONTINUE_SYMBOL = 1


def get_solution_qualities(costs, optimal_cost):
    return [optimal_cost / cost for cost in costs]


def get_intrinsic_value(quality, multiplier):
    return np.multiply(multiplier, quality)


def get_time_cost(step, multiplier):
    return np.exp(np.multiply(multiplier, step))


def get_time_dependent_utility(quality, step, intrinsic_value_multiplier, time_cost_multiplier):
    return get_intrinsic_value(quality, intrinsic_value_multiplier) - get_time_cost(step, time_cost_multiplier)


def get_optimal_stopping_point(comprehensive_values):
    return list(comprehensive_values).index(max(comprehensive_values))


def get_fixed_stopping_point(profile, config):
    best_values = []

    for step in profile.keys():
        expected_value = 0

        for target_class in config["quality_classes"]:
            target_quality = utils.get_bin_value(target_class, config["quality_class_count"])
            comprehensive_value = get_time_dependent_utility(target_quality, step, config["intrinsic_value_multiplier"], config["time_cost_multiplier"])
            expected_value += profile[step][target_class] * comprehensive_value

        best_values.append(expected_value)

    return get_optimal_stopping_point(best_values)


def get_mevc(quality_estimate, time, profile_1, profile_3, config):
    origin_class = utils.digitize(quality_estimate, config["quality_class_bounds"])

    current_expected_value = 0
    next_expected_value = 0

    for target_class in config["quality_classes"]:
        target_quality = utils.get_bin_value(target_class, config["quality_class_count"])

        current_comprehensive_value = get_time_dependent_utility(target_quality, time, config["intrinsic_value_multiplier"], config["time_cost_multiplier"])
        current_expected_value += profile_3[origin_class][time][target_class] * current_comprehensive_value

        next_comprehensive_value = get_time_dependent_utility(target_quality, time + 1, config["intrinsic_value_multiplier"], config["time_cost_multiplier"])
        next_expected_value += profile_1[origin_class][time][target_class] * next_comprehensive_value

    return next_expected_value - current_expected_value


def get_optimal_values(profile_2, profile_3, config, epsilon=0.1):
    limit = len(profile_2[0].keys())
    steps = range(limit)
    
    values = {origin_class: limit * [0] for origin_class in config["quality_classes"]}

    while True:
        new_values = copy.deepcopy(values)

        delta = 0

        for origin_class in config["quality_classes"]:
            for step in steps:
                if step + 1 < limit:
                    stop_value = 0
                    continue_value = 0

                    for target_class in config["quality_classes"]:
                        target_quality = utils.get_bin_value(target_class, config["quality_class_count"])
                        comprehensive_value = get_time_dependent_utility(target_quality, step, config["intrinsic_value_multiplier"], config["time_cost_multiplier"])
                        stop_value += profile_3[origin_class][step][target_class] * comprehensive_value

                        continue_value += profile_2[origin_class][step][target_class] * values[target_class][step + 1]

                    new_values[origin_class][step] = max(stop_value, continue_value)
                    delta = max(delta, abs(new_values[origin_class][step] - values[origin_class][step]))

        values = new_values

        if delta < epsilon:
            return values


def get_optimal_action(quality, step, values, profile_2, profile_3, config):
    origin_class = utils.digitize(quality, config["quality_class_bounds"])

    stop_value = 0
    continue_value = 0

    for target_class in config["quality_classes"]:
        target_quality = utils.get_bin_value(target_class, config["quality_class_count"])
        comprehensive_value = get_time_dependent_utility(target_quality, step, config["intrinsic_value_multiplier"], config["time_cost_multiplier"])
        stop_value += profile_3[origin_class][step][target_class] * comprehensive_value

        continue_value += profile_2[origin_class][step][target_class] * values[target_class][step + 1]

    return STOP_SYMBOL if stop_value >= continue_value else CONTINUE_SYMBOL
