import pygame
import math
import random
from calcs import normalize_angle
from calcs import ang
from calcs import distance


class Endesga:
    maroon_red = (87, 28, 39)
    lighter_maroon_red = (127, 36, 51)
    dark_green = (9, 26, 23)
    light_brown = (191, 111, 74)
    black = (19, 19, 19)
    grey_blue = (66, 76, 110)
    cream = (237, 171, 80)
    white = (255, 255, 255)
    greyL = (200, 200, 200)
    grey = (150, 150, 150)
    greyD = (100, 100, 100)
    greyVD = (50, 50, 50)
    very_light_blue = (199, 207, 221)
    my_blue = [7, 15, 21]


class boid:
    def __init__(self, bx, by, angle, velocity, color, shadow_col, radius, turn_radius, sensing_radius, sensing_distance, proj_number, proj_depth):
        self.x = bx
        self.y = by
        self.a = angle
        self.vel = velocity
        self.color = color
        self.shadow_col = shadow_col
        self.rad = radius
        self.sense = sensing_radius
        self.sense_dist = sensing_distance
        self.turn_radius = turn_radius
        self.proj_number = proj_number
        self.proj_depth = proj_depth
        self.counter = 0
        self.walls = []
        self.rect = pygame.rect.Rect(self.x - self.rad * 2, self.y - self.rad * 2, self.rad * 4, self.rad * 4)

    def attract(self, cords, lever, s, show_arrows):
        angle_to_mouse = normalize_angle(ang((self.x, self.y), cords))
        if lever:
            if normalize_angle(self.a) < angle_to_mouse:
                if math.fabs(angle_to_mouse - normalize_angle(self.a)) < math.pi:
                    self.a += self.turn_radius
                else:
                    self.a -= self.turn_radius
            else:
                if math.fabs(angle_to_mouse - normalize_angle(self.a)) < math.pi:
                    self.a -= self.turn_radius
                else:
                    self.a += self.turn_radius
        if show_arrows:
            pygame.draw.line(s, Endesga.lighter_maroon_red, (self.x, self.y), (self.x + math.cos(angle_to_mouse) * self.rad * 5, self.y + math.sin(angle_to_mouse) * self.rad * 5), 5)

    def avoid(self, walls, s, show_projections, show_hitbox, show_survey_hitbox):
        projections = []
        for depth in range(self.proj_depth):
            for offset in range(self.proj_number):
                normalized_angle_offset = (self.sense / (self.proj_number - 1)) * ((offset + 0.5) - (self.proj_number / 2))
                projections.append([self.x + math.cos(self.a + normalized_angle_offset) * self.sense_dist * ((depth + 1) / self.proj_depth), self.y + math.sin(self.a + normalized_angle_offset) * self.sense_dist * ((depth + 1) / self.proj_depth)])
        if show_projections:
            for proj in projections:
                pygame.draw.line(s, Endesga.very_light_blue, (self.x, self.y), (proj[0], proj[1]), 1)
                pygame.draw.circle(s, Endesga.maroon_red, (proj[0], proj[1]), 5, 0)
        if show_hitbox:
            pygame.draw.rect(s, Endesga.maroon_red, self.rect)
        if show_survey_hitbox:
            for w in self.walls:
                pygame.draw.rect(s, self.color, w)

        self.counter += 1
        if self.counter > 5:
            self.walls = []
            for wall in walls:
                if distance((self.x, self.y), (wall.x, wall.y)) - self.vel * 5 < self.sense_dist:
                    self.walls.append(wall)
            self.counter = 0

        for wall in self.walls:
            for pI, p in enumerate(projections):
                if wall.collidepoint((p[0], p[1])):
                    self.a -= self.turn_radius * math.pow((1 / (1 + pI // self.proj_number)), 1 / 5) * ((pI % self.proj_number) - (self.proj_number / 2) + 0.5) / self.proj_number

    def move_and_blit(self, s):
        self.rect = pygame.rect.Rect(self.x - self.rad * 2, self.y - self.rad * 2, self.rad * 4, self.rad * 4)
        self.x += math.cos(self.a) * self.vel
        self.y += math.sin(self.a) * self.vel
        pygame.draw.polygon(s, self.shadow_col, ((self.x + math.cos(self.a) * self.rad - self.rad / 3, self.y + math.sin(self.a) * self.rad + self.rad / 3),
                                            (self.x + math.cos(self.a - (2 * math.pi / 3)) * self.rad - self.rad / 3, self.y + math.sin(self.a - (2 * math.pi / 3)) * self.rad + self.rad / 3),
                                            (self.x - self.rad / 3, self.y + self.rad / 3),
                                            (self.x + math.cos(self.a + (2 * math.pi / 3)) * self.rad - self.rad / 3, self.y + math.sin(self.a + (2 * math.pi / 3)) * self.rad + self.rad / 3)))

        pygame.draw.polygon(s, self.color, ((self.x + math.cos(self.a) * self.rad, self.y + math.sin(self.a) * self.rad),
                                            (self.x + math.cos(self.a - (2 * math.pi / 3)) * self.rad, self.y + math.sin(self.a - (2 * math.pi / 3)) * self.rad),
                                            (self.x, self.y),
                                            (self.x + math.cos(self.a + (2 * math.pi / 3)) * self.rad, self.y + math.sin(self.a + (2 * math.pi / 3)) * self.rad)))

