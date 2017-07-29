import json

def digitize(item, bins):
    for i, _ in enumerate(bins):
        if i + 1 < len(bins):
            if bins[i] <= item < bins[i + 1]:
                return i
    return len(bins) - 1


def get_bin_value(bin, bin_size):
    length = 1 / bin_size
    offset = length / 2
    return (bin / bin_size) + offset


def get_groups(instances, key):
    return [instance[key] for instance in instances.values()]


def get_max_list_length(lists):
    return max(len(inner_list) for inner_list in lists)


def get_trimmed_lists(groups, max_length):
    trimmed_groups = []

    for solution_qualities in groups:
        trimmed_group = list(solution_qualities)

        while len(trimmed_group) < max_length:
            trimmed_group.append(trimmed_group[-1])

        trimmed_groups.append(trimmed_group)

    return trimmed_groups


def pop(queue):
    minimum_value = float('inf')
    minimum_key = None

    for key in queue:
        if queue[key] < minimum_value:
            minimum_value = queue[key]
            minimum_key = key

    del queue[minimum_key]

    return minimum_key


def load(file_path):
    with open(file_path) as file:
        return json.load(file)


def save(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)
        