import pygame
import math


class Player:
    def __init__(self, x, y, width, height, speed, movement):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.s = speed
        self.m = movement
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

    # left, right, up, down
    def move(self):
        if self.m[0]:
            self.x -= self.s
        if self.m[1]:
            self.x += self.s
        if self.m[2]:
            self.y -= self.s
        if self.m[3]:
            self.y += self.s

    def moveT(self, r):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.m[0]:
            self.x -= self.s
        if self.m[1]:
            self.x += self.s
        if self.m[0] or self.m[1]:
            for tile in r:
                if self.rect.colliderect(tile):
                    if math.fabs(self.x - tile.x + tile.width) < tile.width / 4:
                        self.x = tile.x - tile.width
                    if math.fabs(self.x - tile.x - tile.width) < tile.width / 4:
                        self.x = tile.x + tile.width
        if self.m[2]:
            self.y -= self.s
        if self.m[3]:
            self.y += self.s
        if self.m[2] or self.m[3]:
            for tile in r:
                if self.rect.colliderect(tile):
                    if math.fabs(self.y - tile.y + tile.height) < tile.height / 4:
                        self.y = tile.y - tile.height
                    if math.fabs(self.y - tile.y - tile.height) < tile.height / 4:
                        self.y = tile.y + tile.height

    def draw(self, s, color):
        pygame.draw.rect(s, color, self.rect, 0, 2)
