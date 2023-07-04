import math
import random
import colorsys


def distance(point1, point2):
    return math.sqrt(math.pow(math.fabs(point1[0] - point2[0]), 2) + math.pow(math.fabs(point1[1] - point2[1]), 2))


def ang(start_pos, end_pos):
    if start_pos[0] < end_pos[0]:
        return math.atan((end_pos[1] - start_pos[1]) / (end_pos[0] - start_pos[0] + 0.0001))
    else:
        return math.atan((end_pos[1] - start_pos[1]) / (end_pos[0] - start_pos[0] + 0.0001)) + math.pi


def normalize_angle(angle):
    while angle >= math.pi * 2:
        angle -= math.pi * 2
    while angle <= 0:
        angle += math.pi * 2
    return angle


def collide_circle(point1, point2, d):
    return math.sqrt(math.pow(math.fabs(point1[0] - point2[0]), 2) + math.pow(math.fabs(point1[1] - point2[1]), 2)) < d


def brightness(color, shift):
    output = [0, 0, 0]
    for i, c in enumerate(color):
        output[i] = int(c * shift) + 1
        if output[i] > 255:
            output[i] = 255
    return output


def contrast(color, shift):
    output = [0, 0, 0]
    avg = sum(color) / len(color)
    for i, c in enumerate(color):
        if c > avg:
            output[i] = int(c * (1 + shift))
        if c < avg:
            output[i] = int(c * (1 - shift))
        if c == avg:
            output[i] = c
    for i, o in enumerate(output):
        if o >= 255:
            output[i] = 255
    return output


def shift_hue(color, hue_shift):
    # Convert RGB color to HSV color
    r, g, b = color
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    # Shift the hue
    h = (h + hue_shift) % 1

    # Convert HSV color back to RGB color
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)

    return r, g, b


def random_col():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def normalize(value, minValue, maxValue, doesCap=False):
    output = (value - minValue) / (maxValue - minValue)
    if doesCap:
        if output > 1:
            output = 1
        if output < 0:
            output = 0
    return output


def cap(value, minValue, maxValue):
    if value > maxValue:
        value = maxValue
    if value < minValue:
        value = minValue
    return value

