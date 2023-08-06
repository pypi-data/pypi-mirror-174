# Utility functions


def simple_function(test):
    return test + 1


def mean_function(test):
    count = 0
    total = 0
    for val in test:
        total += val
        count += 1
    return total / count


def max_function(test):
    if not test:
        return -1

    max_value = 0
    for val in test:
        if val > max_value:
            max_value = val
    return max_value


def min_function(test):
    if not test:
        return -1

    min_value = test[0]
    for val in test[1:]:
        if val < min_value:
            min_value = val
    return min_value
