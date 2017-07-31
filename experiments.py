import json
import os

import computation
import monitor
import tsp


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
