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
