import math
import random
import colorsys


def distance(point1, point2):
    return math.sqrt(math.pow(math.fabs(point1[0] - point2[0]), 2) + math.pow(math.fabs(point1[1] - point2[1]), 2))


def ang(start_pos, end_pos):
    return math.atan((end_pos[1] - start_pos[1]) / (end_pos[0] - start_pos[0] + 0.0001)) + math.pi * (1 - (start_pos[0] <= end_pos[0]))


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


def linear_gradient(colors, normalizedZero2One):
    percent = round(10000 * ((len(colors) - 1) * normalizedZero2One % 1)) / 10000
    index = int(math.fabs((len(colors) - 1) * normalizedZero2One - 0.0000001))
    return [int(colors[index][0] + percent * (colors[index + 1][0] - colors[index][0])),
            int(colors[index][1] + percent * (colors[index + 1][1] - colors[index][1])),
            int(colors[index][2] + percent * (colors[index + 1][2] - colors[index][2]))]


def normalize(value, minValue, maxValue, doesCap=False):
    output = (value - minValue) / (maxValue - minValue)
    if doesCap:
        if output > 1:
            output = 1
        if output < 0:
            output = 0
    return output


def clip(minVal, maxVal, val):
    return min(maxVal, max(minVal, val))


def point_to_line(point, two_points_of_line):
    point_x, point_y = point
    x1, y1 = two_points_of_line[0]
    x2, y2 = two_points_of_line[1]
    dx = x2 - x1
    dy = y2 - y1
    parameterization = ((point_x - x1) * dx + (point_y - y1) * dy) / (dx ** 2 + dy ** 2)
    if parameterization < 0:
        closest_x, closest_y = x1, y1
    elif parameterization > 1:
        closest_x, closest_y = x2, y2
    else:
        closest_x = x1 + parameterization * dx
        closest_y = y1 + parameterization * dy

    d = math.sqrt((point_x - closest_x) ** 2 + (point_y - closest_y) ** 2)
    return d, [closest_x, closest_y]


def circumcircle(vertices):
    # Extract the vertices
    (x1, y1), (x2, y2), (x3, y3) = vertices

    # Calculate the coordinates of the circumcircle center
    D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    center_x = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / D
    center_y = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / D

    # Calculate the radius of the circumcircle
    radius = math.sqrt((x1 - center_x) ** 2 + (y1 - center_y) ** 2)

    return (center_x, center_y), radius


def random_sign():
    return random.randint(0, 1) * 2 - 1
