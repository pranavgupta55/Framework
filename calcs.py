import math
import random


def distance(point1, point2):
    return math.sqrt(math.pow(math.fabs(point1[0] - point2[0]), 2) + math.pow(math.fabs(point1[1] - point2[1]), 2))
