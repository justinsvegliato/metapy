import json
import os

import computation
import monitor
import tsp
import performance
import utils

import numpy as np

TIME_COST_MULTIPLIER = 0.1
INTRINSIC_VALUE_MULTIPLIER = 200
SOLUTION_QUALITY_CLASS_COUNT = 5
SOLUTION_QUALITY_CLASS_BOUNDS = np.linspace(0, 1, SOLUTION_QUALITY_CLASS_COUNT + 1)
SOLUTION_QUALITY_CLASSES = range(SOLUTION_QUALITY_CLASS_COUNT)

CONFIG = {
    "time_cost_multiplier": TIME_COST_MULTIPLIER,
    "intrinsic_value_multiplier": INTRINSIC_VALUE_MULTIPLIER,
    "quality_classes": SOLUTION_QUALITY_CLASSES,
    "quality_class_bounds": SOLUTION_QUALITY_CLASS_BOUNDS,
    "quality_class_count": SOLUTION_QUALITY_CLASS_COUNT
}


def get_optimal_costs(file_path):
    with open(file_path) as file:
        entries = [line.strip().split(",") for line in file.readlines()]
        return {entry[0]: float(entry[1]) for entry in entries}


def get_simulations(instances_directory, index_file_path):
    optimal_costs = get_optimal_costs(index_file_path)

    performances = {}

    for file in os.listdir(instances_directory):
        if file.endswith(".tsp"):
            print("Handling %s..." % file)

            instance = os.path.splitext(file)[0]
            file_path = os.path.join(instances_directory, file)

            states, start_state = tsp.load_instance(file_path)
            costs = monitor.recorder(tsp.k_opt_solve, states, start_state, 1000)

            optimal_cost = optimal_costs[instance]
            qualities = computation.get_solution_qualities(costs, optimal_cost)

            heuristic_cost = tsp.get_mst_distance(start_state, states)
            estimated_qualities = computation.get_solution_qualities(costs, heuristic_cost)

            performances[instance] = {
                "qualities": qualities,
                "estimated_qualities": estimated_qualities
            }

    return performances


def experiment_1(simulations_file, instances_directory):
    simulations = utils.load("problems/50-tsp/simulations.json")

    profile_1 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_1)
    profile_2 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_2)
    profile_3 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_3)
    profile_4 = performance.get_probabilistic_performance_profile(simulations, CONFIG)

    fixed_losses = []
    myopic_losses = []
    nonmyopic_losses = []
    projected_losses = []

    for file in os.listdir(instances_directory):
        if file.endswith(".tsp"):
            print("Experiment: %s" % file)

            instance = os.path.splitext(file)[0]
            file_path = os.path.join(instances_directory, file)

            true_qualities = simulations[instance]["qualities"]
            true_comprehensive_values = computation.get_time_dependent_utility(true_qualities, range(len(true_qualities)), INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)

            optimal_stopping_point = computation.get_optimal_stopping_point(true_comprehensive_values)
            optimal_comprehensive_value = true_comprehensive_values[optimal_stopping_point]

            states, start_state = tsp.load_instance(file_path)

            heuristic = tsp.get_mst_distance(start_state, states)
            quality_estimator = lambda cost: heuristic / cost

            print("Fixed Monitor:")
            _, fixed_records = monitor.fixed_monitor(tsp.k_opt_solve, quality_estimator, profile_4, CONFIG, states, start_state, 1000)
            fixed_comprehensive_value = computation.get_time_dependent_utility(fixed_records[-1]['q'], fixed_records[-1]['t'], INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            fixed_losses.append(utils.get_percent_error(optimal_comprehensive_value, fixed_comprehensive_value))

            print("Myopic Monitor:")
            _, myopic_records = monitor.myopic_monitor(tsp.k_opt_solve, quality_estimator, profile_1, profile_3, CONFIG,  states, start_state, 1000)
            myopic_comprehensive_value = computation.get_time_dependent_utility(myopic_records[-1]['q'], myopic_records[-1]['t'], INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            myopic_losses.append(utils.get_percent_error(optimal_comprehensive_value, myopic_comprehensive_value))

            print("Nonmyopic Monitor:")
            _, nonmyopic_records = monitor.nonmyopic_monitor(tsp.k_opt_solve, quality_estimator, profile_2, profile_3, CONFIG, states, start_state, 1000)
            nonmyopic_comprehensive_value = computation.get_time_dependent_utility(nonmyopic_records[-1]['q'], nonmyopic_records[-1]['t'], INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            nonmyopic_losses.append(utils.get_percent_error(optimal_comprehensive_value, nonmyopic_comprehensive_value))

            print("Projected Monitor:")
            _, projected_records = monitor.projected_monitor(tsp.k_opt_solve, quality_estimator, CONFIG, states, start_state, 1000)
            projected_comprehensive_value = computation.get_time_dependent_utility(projected_records[-1]['q'], projected_records[-1]['t'], INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            projected_losses.append(utils.get_percent_error(optimal_comprehensive_value, projected_comprehensive_value))
        

    print("Fixed Time Allocation Average Percent Error: %f%%" % np.average(fixed_losses))
    print("Myopic Monitoring Average Percent Error: %f%%" % np.average(myopic_losses))
    print("Nonmyopic Monitoring Average Percent Error: %f%%" % np.average(nonmyopic_losses))
    print("Projected Monitoring Average Percent Error: %f%%" % np.average(projected_losses))


def main():
    experiment_1("problems/50-tsp/simulations.json", "problems/50-tsp")


main()