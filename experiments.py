import os

import computation
import monitor
import tsp
import utils

ITERATIONS = 2000


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
            costs = monitor.recorder(tsp.k_opt_solve, states, start_state, ITERATIONS)

            optimal_cost = optimal_costs[instance]
            qualities = computation.get_solution_qualities(costs, optimal_cost)

            heuristic_cost = tsp.get_mst_distance(start_state, states)
            estimated_qualities = computation.get_solution_qualities(costs, heuristic_cost)

            performances[instance] = {
                "qualities": qualities,
                "estimated_qualities": estimated_qualities
            }

    return performances


def main():
    simulations = get_simulations("problems/100-tsp", "problems/100-tsp/instances.csv")
    utils.save(simulations, "simulations/100-tsp-0.1s.json")

    # for i in range(50):
    #     cities = tsp.get_instance(100, 0, 10000, 1)
    #     tsp.save_instance('problems/100-tsp/instance-%d.tsp' % i, cities)

main()
