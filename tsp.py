import itertools
import random
import re
import sys

import numpy as np

import utils

FILE_TEMPLATE = '''NAME : %s
COMMENT : %s
TYPE : TSP
DIMENSION: %d
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
%s
EOF
'''
CITY_TEMPLATE = '%d %i %i %s'
COMMENT = 'No Comment'
CITY_PATTERN = '\d+ (\d+) (\d+)'
DELIMITER = '\n'


def get_initial_random_tour(states, start_state):
    adjustable_states = set(states) - set([start_state])
    return [start_state] + list(np.random.permutation(list(adjustable_states))) + [start_state]


def get_swappable_cities(tour):
    return range(1, len(tour) - 1)


def get_mutated_tour(tour, first_key, second_key):
    mutated_tour = list(tour)
    mutated_tour[first_key], mutated_tour[second_key] = mutated_tour[second_key], mutated_tour[first_key]
    return mutated_tour


def get_distance(first_city, second_city):
    return np.linalg.norm(np.subtract(first_city, second_city))


def get_tour_distance(tour):
    distance = 0

    for i in range(len(tour)):
        if i + 1 == len(tour):
            break

        distance += get_distance(tour[i], tour[i + 1])

    return distance


def k_opt_solve(states, start_state, iterations, memory):
    tour = get_initial_random_tour(states, start_state)
    cities = get_swappable_cities(tour)
    distance = get_tour_distance(tour)

    for _ in range(iterations):
        has_changed = False

        best_tour = tour
        best_distance = distance
        for first_key, second_key in itertools.combinations(cities, 2):
            current_tour = get_mutated_tour(tour, first_key, second_key)
            current_distance = get_tour_distance(current_tour)

            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance

                memory['solution'] = current_tour
                memory['cost'] = best_distance                

                has_changed = True

        tour = best_tour
        distance = best_distance

        if not has_changed:
            break

    return tour


def get_graph(cities):
    graph = {}

    for start_city in cities:
        graph[start_city] = {}

        for end_city in cities:
            graph[start_city][end_city] = get_distance(start_city, end_city)

    return graph


def get_nearest_city_distance(start_city, cities):
    nearest_distance = float('inf')

    for city in cities:
        if start_city == city:
            continue

        current_city_distance = get_distance(start_city, city)
        if current_city_distance < nearest_distance:
            nearest_distance = current_city_distance

    return nearest_distance


def get_mst_distance(start_city, cities):
    subset = cities - set([start_city])
    graph = get_graph(subset)

    predecessors = {}
    key = {}
    queue = {}

    for vertex in graph:
        predecessors[vertex] = -1
        key[vertex] = sys.maxsize

    key[start_city] = 0

    for vertex in graph:
        queue[vertex] = key[vertex]

    while queue:
        city = utils.pop(queue)

        for vertex in graph[city]:
            if vertex in queue and graph[city][vertex] < key[vertex]:
                predecessors[vertex] = city
                key[vertex] = graph[city][vertex]
                queue[vertex] = graph[city][vertex]

    cost = 0
    for parent_city in predecessors:
        child_city = predecessors[parent_city]
        if child_city != -1:
            cost += get_distance(parent_city, child_city)

    return cost + 2 * get_nearest_city_distance(start_city, cities)


def get_instance(size, start_position, end_position, minimum_distance):
    choices = np.arange(start_position, end_position, minimum_distance)

    cities = set()
    while len(cities) < size:
        x = round(random.choice(choices), 3)
        y = round(random.choice(choices), 3)
        cities.add((x, y))

    return cities


def save_instance(name, comment, cities):
    size = len(cities)

    node_coord_section = ''
    for i, city in enumerate(cities):
        x, y = city
        delimiter = DELIMITER if i < size - 1 else ''
        node_coord_section += CITY_TEMPLATE % (i + 1, x, y, delimiter)

    instance = FILE_TEMPLATE % (name, comment, size, node_coord_section)

    f = open(name, 'w')
    f.write(instance)
    f.close()


def load_instance(filename):
    cities = set()

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(CITY_PATTERN, line)
            if match:
                x = float(match.groups()[0])
                y = float(match.groups()[1])
                cities.add((x, y))

    start_city = list(cities)[0]

    return cities, start_city
