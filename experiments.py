import os

import computation
import monitor
import qap
import tsp
import jsp
import utils

ITERATIONS = 2000


def get_tsp_simulations(instances_directory, index_file_path):
    optimal_costs = utils.get_csv_dictionary(index_file_path)

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


def get_qap_simulations(instances_directory, lower_bound_path):
    lower_bounds = utils.get_csv_dictionary(lower_bound_path)

    performances = {}

    for file in os.listdir(instances_directory):
        if file.endswith('.results'):
            print("Handling %s..." % file)

            instance = os.path.splitext(file)[0].split('.')[0]
            file_path = os.path.join(instances_directory, file)

            f = open(file_path)
            costs = [float(line.strip()) for line in f.readlines()]
            f.close()

            lower_bound = lower_bounds[instance]
            estimated_qualities = computation.get_solution_qualities(costs, lower_bound)

            performances[instance] = {
                "qualities": estimated_qualities,
                "estimated_qualities": estimated_qualities
            }

    return performances


def get_adapted_qap_simulations(simulation_path):
    simulations = utils.load(simulation_path)

    for key in simulations:
        simulations[key]['qualities'] = simulations[key]['estimated_qualities']

    return simulations


def main():
    # simulations = get_tsp_simulations("problems/100-tsp", "problems/100-tsp/instances.csv")
    # utils.save(simulations, "simulations/100-tsp-0.1s.json")

    # for i in range(50):
    #     cities = tsp.get_instance(100, 0, 10000, 1)
    #     tsp.save_instance('problems/100-tsp/instance-%d.tsp' % i, cities)

    # simulations = get_qap_simulations("problems/50-qap", "problems/50-qap/lower-bounds.csv")
    # utils.save(simulations, "simulations/50-qap.json")

    # for i in range(50):
    #     size, weight_matrix, distance_matrix = qap.generate_instance(50)
    #     qap.save_instance('problems/50-qap/instance-%d.dat' % i, size, weight_matrix, distance_matrix)

    # for i in range(50):
    #     instance = jsp.generate_instance(10, 10, 100)
    #     f = open('problems/10-10-100-jsp/instance-%d.txt' % i, 'w')
    #     f.write(instance)
    #     f.close()




if __name__ == '__main__':
    main()
