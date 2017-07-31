import performance
import data
import numpy as np
import utils
import monitor
import tsp
import computation

# simulations = data.get_simulations("problems/50-tsp", "problems/50-tsp/index.csv")
# utils.save(simulations, "problems/50-tsp/simulations.json")

states, start_state = tsp.load_instance("problems/50-tsp/instance-30.tsp")


simulations = utils.load("problems/50-tsp/simulations.json")

profile_1 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_1)
profile_2 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_2)
profile_3 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_3)
profile_4 = performance.get_probabilistic_performance_profile(simulations, CONFIG)

heuristic = tsp.get_mst_distance(start_state, states)
quality_estimator = lambda cost: heuristic / cost

# true_qualities = simulations["instance-30"]["qualities"]
# intrinsic_values = computation.get_intrinsic_value(true_qualities, INTRINSIC_VALUE_MULTIPLIER) - computation.get_time_cost(range(len(true_qualities)), TIME_COST_MULTIPLIER)
# optimal_stopping_point = computation.get_optimal_stopping_point(intrinsic_values)
# print(optimal_stopping_point)

# print("Recorder:")
# monitor.recorder(tsp.k_opt_solve, states, start_state, 1000)

print("Fixed Monitor:")
monitor.fixed_monitor(tsp.k_opt_solve, quality_estimator, profile_4, CONFIG, states, start_state, 1000)

print("Myopic Monitor:")
monitor.myopic_monitor(tsp.k_opt_solve, quality_estimator, profile_1, profile_3, CONFIG,  states, start_state, 1000)

print("Nonmyopic Monitor:")
monitor.nonmyopic_monitor(tsp.k_opt_solve, quality_estimator, profile_2, profile_3, CONFIG, states, start_state, 1000)