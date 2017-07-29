import performance
import data
import numpy as np
import utils
import monitor
import tsp

simulations = utils.load("problems/50-tsp/simulations.json")

TIME_COST_MULTIPLIER = 0.00005
INTRINSIC_VALUE_MULTIPLIER = 200
SOLUTION_QUALITY_CLASS_COUNT = 5
SOLUTION_QUALITY_CLASS_BOUNDS = np.linspace(0, 1, SOLUTION_QUALITY_CLASS_COUNT + 1)
SOLUTION_QUALITY_CLASSES = range(SOLUTION_QUALITY_CLASS_COUNT)

CONFIG = {
    'time_cost_multiplier': TIME_COST_MULTIPLIER,
    'intrinsic_value_multiplier': INTRINSIC_VALUE_MULTIPLIER,
    'quality_classes': SOLUTION_QUALITY_CLASSES,
    'quality_class_bounds': SOLUTION_QUALITY_CLASS_BOUNDS,
    'quality_class_count': SOLUTION_QUALITY_CLASS_COUNT
}
profile_1 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_1)
profile_3 = performance.get_dynamic_performance_profile(simulations, CONFIG, performance.TYPE_3)

states, start_state = tsp.load_instance("problems/50-tsp/instance-30.tsp")
monitor.myopic_monitor(tsp.k_opt_solve, states, start_state, profile_1, profile_3, CONFIG)