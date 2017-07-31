import json
import os

import computation
import monitor
import tsp
import performance
import matplotlib.pyplot as plt
import utils

import numpy as np

TIME_COST_MULTIPLIER = 0.15
INTRINSIC_VALUE_MULTIPLIER = 200
SOLUTION_QUALITY_CLASS_COUNT = 20
SOLUTION_QUALITY_CLASS_BOUNDS = np.linspace(0, 1, SOLUTION_QUALITY_CLASS_COUNT + 1)
SOLUTION_QUALITY_CLASSES = range(SOLUTION_QUALITY_CLASS_COUNT)

CONFIG = {
    "time_cost_multiplier": TIME_COST_MULTIPLIER,
    "intrinsic_value_multiplier": INTRINSIC_VALUE_MULTIPLIER,
    "quality_classes": SOLUTION_QUALITY_CLASSES,
    "quality_class_bounds": SOLUTION_QUALITY_CLASS_BOUNDS,
    "quality_class_count": SOLUTION_QUALITY_CLASS_COUNT
}

TOUR_SIZE = 50


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
            true_steps = range(len(true_qualities))
            true_comprehensive_values = computation.get_time_dependent_utility(true_qualities, true_steps, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)

            optimal_stopping_point = computation.get_optimal_stopping_point(true_comprehensive_values)
            optimal_comprehensive_value = true_comprehensive_values[optimal_stopping_point]

            states, start_state = tsp.load_instance(file_path)

            heuristic = tsp.get_mst_distance(start_state, states)
            quality_estimator = lambda cost: heuristic / cost

            print("Fixed Monitor:")
            _, fixed_records = monitor.fixed_monitor(tsp.k_opt_solve, quality_estimator, profile_4, CONFIG, states, start_state, 1000)
            fixed_qualities = [record['q'] for record in fixed_records]
            fixed_points = [record['t'] for record in fixed_records]
            fixed_comprehensive_values = computation.get_time_dependent_utility(fixed_qualities, fixed_points, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            fixed_quality = fixed_records[-1]['q']
            fixed_point = fixed_records[-1]['t']
            fixed_comprehensive_value = computation.get_time_dependent_utility(fixed_quality, fixed_point, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            fixed_losses.append(utils.get_percent_error(optimal_comprehensive_value, fixed_comprehensive_value))

            print("Myopic Monitor:")
            _, myopic_records = monitor.myopic_monitor(tsp.k_opt_solve, quality_estimator, profile_1, profile_3, CONFIG,  states, start_state, 1000)
            myopic_qualities = [record['q'] for record in myopic_records]
            myopic_points = [record['t'] for record in myopic_records]
            myopic_comprehensive_values = computation.get_time_dependent_utility(myopic_qualities, myopic_points, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            myopic_quality = myopic_records[-1]['q']
            myopic_point = myopic_records[-1]['t']
            myopic_comprehensive_value = computation.get_time_dependent_utility(myopic_quality, myopic_point, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            myopic_losses.append(utils.get_percent_error(optimal_comprehensive_value, myopic_comprehensive_value))

            print("Nonmyopic Monitor:")
            _, nonmyopic_records = monitor.nonmyopic_monitor(tsp.k_opt_solve, quality_estimator, profile_2, profile_3, CONFIG, states, start_state, 1000)
            nonmyopic_qualities = [record['q'] for record in nonmyopic_records]
            nonmyopic_points = [record['t'] for record in nonmyopic_records]
            nonmyopic_comprehensive_values = computation.get_time_dependent_utility(nonmyopic_qualities, nonmyopic_points, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            nonmyopic_quality = nonmyopic_records[-1]['q']
            nonmyopic_point = nonmyopic_records[-1]['t']
            nonmyopic_comprehensive_value = computation.get_time_dependent_utility(nonmyopic_quality, nonmyopic_point, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            nonmyopic_losses.append(utils.get_percent_error(optimal_comprehensive_value, nonmyopic_comprehensive_value))

            print("Projected Monitor:")
            _, projected_records = monitor.projected_monitor(tsp.k_opt_solve, quality_estimator, CONFIG, states, start_state, 1000)
            projected_qualities = [record['q'] for record in projected_records]
            projected_points = [record['t'] for record in projected_records]
            projected_comprehensive_values = computation.get_time_dependent_utility(projected_qualities, projected_points, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            projected_quality = projected_records[-1]['q']
            projected_point = projected_records[-1]['t'] 
            projected_comprehensive_value = computation.get_time_dependent_utility(projected_quality, projected_point, INTRINSIC_VALUE_MULTIPLIER, TIME_COST_MULTIPLIER)
            projected_losses.append(utils.get_percent_error(optimal_comprehensive_value, projected_comprehensive_value))
            
            plt.figure(figsize=(16, 12), dpi=80)
            plt.title('Performance Profile')
            plt.xlabel('Time')
            plt.ylabel('Value')

            plt.annotate('%d-TSP' % TOUR_SIZE, xy=(0, 0), xytext=(10, 172), va='bottom', xycoords='axes fraction', textcoords='offset points')
            plt.annotate('%d Discrete Solution Qualities' % SOLUTION_QUALITY_CLASS_COUNT, xy=(0, 0), xytext=(10, 162), va='bottom', xycoords='axes fraction', textcoords='offset points')
            plt.annotate('$q(s) = Length_{MST} / Length(s)$', xy=(0, 0), xytext=(10, 152), va='bottom', xycoords='axes fraction', textcoords='offset points')
            plt.annotate('$U_C(t) = -e^{%.2ft}$' % TIME_COST_MULTIPLIER, xy=(0, 0), xytext=(10, 135), va='bottom', xycoords='axes fraction', textcoords='offset points')
            plt.annotate('$U_I(q) = %dq$' % INTRINSIC_VALUE_MULTIPLIER, xy=(0, 0), xytext=(10, 125), va='bottom', xycoords='axes fraction', textcoords='offset points')
            plt.annotate('$U(q, t) = U_C(t) - U_I(q)$', xy=(0, 0), xytext=(10, 115), va='bottom', xycoords='axes fraction', textcoords='offset points')

            plt.plot(true_steps, true_comprehensive_values, color='g', zorder=3, label='True Comprehensive Values')
            plt.plot(fixed_points, fixed_comprehensive_values, color='g', zorder=3, label='Fixed Comprehensive Values')
            plt.plot(myopic_points, myopic_comprehensive_values, color='g', zorder=3, label='Myopic Comprehensive Values')
            plt.plot(nonmyopic_points, nonmyopic_comprehensive_values, color='g', zorder=3, label='Nonmyopic Comprehensive Values')
            plt.plot(projected_points, projected_comprehensive_values, color='g', zorder=3, label='Projected Comprehensive Values')

            plt.scatter([optimal_stopping_point], optimal_comprehensive_value, color='limegreen', zorder=4, label='Optimal Stopping Point')
            plt.scatter([projected_point], projected_comprehensive_value, color='m', zorder=4, label='Projected Stopping Point')
            plt.scatter([nonmyopic_point], nonmyopic_comprehensive_value, color='maroon', zorder=4, label='Nonmyopic Stopping Point')
            plt.scatter([myopic_point], myopic_comprehensive_value, color='y', zorder=4, label='Myopic Stopping Point')
            plt.scatter([fixed_point], fixed_comprehensive_value, color='c', zorder=4, label='Fixed Stopping Point')

            plt.legend(bbox_to_anchor=(0.0, 1.04, 1.0, 0.102), loc=3, ncol=3, mode='expand', borderaxespad=0.0)

            filename = 'plots/' + instance + '.png'
            plt.savefig(filename)
            plt.close()
        

    print("Fixed Time Allocation Average Percent Error: %f%%" % np.average(fixed_losses))
    print("Myopic Monitoring Average Percent Error: %f%%" % np.average(myopic_losses))
    print("Nonmyopic Monitoring Average Percent Error: %f%%" % np.average(nonmyopic_losses))
    print("Projected Monitoring Average Percent Error: %f%%" % np.average(projected_losses))


def main():
    experiment_1("problems/50-tsp/simulations.json", "problems/50-tsp")


main()