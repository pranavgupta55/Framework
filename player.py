import pygame
import math
from calcs import distance


class Player:
    def __init__(self, x, y, w, h, speed, jump_height, max_jumps=2, gravity=0.2, color=(255, 255, 255), momentum=1.0, terminal_vel=7, hp=0, dmg=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.m = momentum
        self.s = speed
        self.vel = [0, 0]
        self.jh = jump_height
        self.hp = hp
        self.col = color
        self.dmg = dmg
        self.dir = [0, 0]
        self.max_jumps = max_jumps
        self.jump_counter = max_jumps
        self.sample_counter = 0
        self.sample_rate = 10
        self.walls = []
        self.g = gravity
        self.tv = terminal_vel

    def update(self, ts, delta_t):
        self.sample_counter += delta_t
        if self.sample_counter > self.sample_rate:
            self.walls = []
            for ti in ts:
                if distance((ti.centerx, ti.centery), (self.rect.centerx, self.rect.centery)) < (2 * max([math.fabs(self.vel[0]), math.fabs(self.vel[1]), self.tv]) * self.sample_rate):
                    self.walls.append(ti)
            self.sample_counter = 0

    def move(self, delta_t):
        self.vel[0] *= (1 - self.m)
        self.vel[0] += self.m * self.s * self.dir[0] * delta_t
        self.x += self.vel[0] * delta_t
        self.rect.x = self.x
        for w in self.walls:
            if w.colliderect(self.rect):
                if self.dir[0] > 0:
                    self.x = w.left - self.rect.width - 1
                    self.vel[0] = 0
                elif self.dir[0] < 0:
                    self.x = w.right + 1
                    self.vel[0] = 0
        self.rect.x = self.x
        self.vel[1] += self.g
        if self.vel[1] > self.tv:
            self.vel[1] = self.tv
        self.y += self.vel[1]
        self.rect.y = self.y
        for w in self.walls:
            if w.colliderect(self.rect):
                if self.vel[1] > 0:
                    self.jump_counter = self.max_jumps
                    self.y = w.top - self.rect.height
                    self.vel[1] = 0
                elif self.vel[1] < 0:
                    self.y = w.bottom + 1
                    self.vel[1] = 0
        self.rect.y = self.y

    def jump(self):
        if self.jump_counter > 0:
            self.vel[1] = -self.jh
        self.jump_counter -= 1

    def draw(self, s, scroll, show_rects, show_hitbox):
        pygame.draw.rect(s, self.col, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 0, int(min(self.rect.w, self.rect.h) / 4))
        if show_rects:
            for w in self.walls:
                pygame.draw.rect(s, [255, 96, 141], (w.x - scroll[0], w.y - scroll[1], w.w, w.h))
        if show_hitbox:
            pygame.draw.rect(s, [255, 96, 141], (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 1)
