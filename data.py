import os
import monitor
import tsp
import tsp_solver
import json


def get_optimal_costs(file_path):
    with open(file_path) as file:
        entries = [line.strip().split(",") for line in file.readlines()]
        return {entry[0]: float(entry[1]) for entry in entries}


def get_performances(instances_directory, index_file_path):
    optimal_costs = get_optimal_costs(index_file_path)

    performances = {}
    for file in os.listdir(instances_directory):
        if file.endswith(".tsp"):
            print("Handling %s" % file)

            instance = os.path.splitext(file)[0]
            file_path = os.path.join(instances_directory, file)

            states, start_state = tsp.load_instance(file_path)
            checkpoints = monitor.recorder(tsp_solver.k_opt_solve, states, start_state, 1000)
            optimal_cost = optimal_costs[instance]
            performances[instance] = [(checkpoint[0], optimal_cost / checkpoint[1]) for checkpoint in checkpoints]
            break

    return performances

def main():
    performances = get_performances("problems/50-tsp", "problems/50-tsp/index.csv")
    print(json.dumps(performances))


if __name__ == "__main__":
    main()
