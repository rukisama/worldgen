import math


def normalize(oldmax, oldmin, newmax, newmin, x):
    result = (newmax - newmin) * ((x - oldmin) / (oldmax - oldmin)) + newmin

    return result
