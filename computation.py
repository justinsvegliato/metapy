import utils


def get_intrinsic_value(quality, multiplier=1):
    return multiplier * quality


def get_time_cost(time, multiplier=1):
    return multiplier * time


def get_comprehensive_value(instrinsic_value, time_cost):
    return instrinsic_value - time_cost


def get_mevc(quality_estimate, time, profile_1, profile_3, config):
    origin_class = utils.digitize(quality_estimate, config['solution_quality_class_bounds'])

    current_time_cost = get_time_cost(time, config['time_cost_multiplier'])
    next_time_cost = get_time_cost(time + 1, config['time_cost_multiplier'])

    current_expected_value = 0
    next_expected_value = 0

    for target_class in config['solution_quality_classes']:
        target_quality = utils.get_bin_value(target_class, config['solution_quality_class_count'])
        target_intrinsic_value = get_intrinsic_value(target_quality, config['intrinsic_value_multiplier'])

        current_comprehensive_value = get_comprehensive_value(target_intrinsic_value, current_time_cost)
        current_expected_value += profile_3[origin_class][time][target_class] * current_comprehensive_value

        next_comprehensive_value = get_comprehensive_value(target_intrinsic_value, next_time_cost)
        next_expected_value += profile_1[origin_class][time][target_class] * next_comprehensive_value

    return next_expected_value - current_expected_value
