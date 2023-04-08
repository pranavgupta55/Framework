import pygame
import math


class slider:
    def __init__(self, x, y, width, height, orientation):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.click = False
        self.o = orientation
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.bar = 0

    def detect(self, clik, x, y):
        if clik:
            if self.rect.collidepoint((x, y)):
                if self.o == "ver":
                    self.bar = y - self.y
                    return math.fabs(self.bar / self.h)
                if self.o == "hor":
                    self.bar = x - self.x
                    return math.fabs(self.bar / self.w)

    def draw(self, display_screen, color, bar_color):
        if self.o == "ver":
            pygame.draw.rect(display_screen, bar_color, pygame.rect.Rect(self.x, self.y, self.w, self.bar), 0, math.floor(self.w / 4))
            pygame.draw.rect(display_screen, color, self.rect, int(self.w / 10), math.floor(self.w / 4))
        if self.o == "hor":
            pygame.draw.rect(display_screen, bar_color, pygame.rect.Rect(self.x, self.y, self.bar, self.h), 0, math.floor(self.h / 4))
            pygame.draw.rect(display_screen, color, self.rect, int(self.h / 10), math.floor(self.h / 4))
