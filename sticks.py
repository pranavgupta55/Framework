import math
import pygame
import copy
import numpy as np
from calcs import ang
from calcs import normalize_angle


class point:
    def __init__(self, pos, locked=False):
        self.pos = pos
        self.locked = locked


class stick:
    def __init__(self, centerPos, rad, locked, stick_col=(255, 255, 255), point_col=(20, 20, 20), angle=0):
        self.a = angle
        self.center = centerPos
        self.rad = rad
        self.stick_col = stick_col
        self.point_col = point_col
        self.points = np.array([[self.center[0] - self.rad * math.cos(self.a), self.center[1] - self.rad * math.sin(self.a)], [self.center[0] + self.rad * math.cos(self.a), self.center[1] + self.rad * math.sin(self.a)]])
        self.prev = self.points
        self.locked = np.array(locked)
        self.vels = np.array([[0.0, 0.0], [0.0, 0.0]])

    def update(self, dt, gravity):
        self.vels = self.points - self.prev
        self.vels[:, 1] += dt * gravity
        self.prev = copy.deepcopy(self.points)
        self.points += self.vels
        self.center = sum(self.points) / 2
        self.a = normalize_angle(ang(self.points[0], self.points[1]))
        self.points[0] = [self.center[0] - math.cos(self.a) * self.rad, self.center[1] - math.sin(self.a) * self.rad]
        self.points[1] = [self.center[0] + math.cos(self.a) * self.rad, self.center[1] + math.sin(self.a) * self.rad]

    def draw(self, s, velocity_arrow_color=(255, 150, 200), velocity_arrow_size_multiplier=5):
        pygame.draw.line(s, self.stick_col, self.points[0], self.points[1])
        for i, p in enumerate(self.points):
            pygame.draw.line(s, velocity_arrow_color, p, p + velocity_arrow_size_multiplier * self.vels[i])
            pygame.draw.circle(s, self.point_col, p, 3)
