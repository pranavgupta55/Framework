import pygame
import math
from calcs import distance
from calcs import normalize_angle
fps = 60
tile_size = 20


class shockwave:
    # Function for initializing the shockwave object with its parameters
    def __init__(self, sx, sy, duration, size, max_size, width, color, color2, shadow):
        self.x = sx
        self.y = sy
        self.duration = duration
        self.size = size
        self.max_size = max_size
        self.width = width
        self.color = color
        self.color2 = color2
        self.shadow = shadow

    # This function is run each frame and increases the size of the shockwave but decreases the width
    def expand(self):
        self.size += (self.max_size-self.size)/(10 * self.duration)
        if self.size/self.max_size < 0.8:
            self.width -= 0.03
        else:
            self.width -= 0.1

    # This function draws the shockwave (and its shadow) on the screen
    def blit(self, s):
        pygame.draw.circle(s, self.color2, (self.x - self.shadow, self.y + self.shadow), self.size, int(self.width))
        pygame.draw.circle(s, self.color, (self.x, self.y), self.size, int(self.width))


class particle:
    def __init__(self, px, py, vel, a, color, color2, size, decay, gravity, bounciness, timer):
        self.x = px
        self.y = py
        self.vel = vel
        self.a = a
        self.size = size
        self.rect = pygame.rect.Rect(self.x - self.size / 2, self.y - self.size / 2, self.size, self.size)
        self.color = color
        self.color2 = color2
        self.decay = decay
        self.gravity = gravity
        self.bounciness = bounciness
        self.walls = []
        self.timer = timer
        self.sample_counter = 0
        self.sample_rate = 2
        self.dir = [1, 1]

    def update(self, ts, tile_s, delta_t):
        self.a = normalize_angle(self.a)
        if 0 < self.a < math.pi / 2:
            self.a += self.gravity
        if math.pi / 2 < self.a < math.pi:
            self.a -= self.gravity
        if math.pi < self.a < 3 * math.pi / 4:
            self.a -= self.gravity
        if 3 * math.pi / 4 < self.a < math.pi * 2:
            self.a += self.gravity
        self.size -= self.decay
        self.timer -= 1 * delta_t
        self.sample_counter += 1
        if self.sample_counter > self.sample_rate:
            self.walls = []
            for ti in ts:
                if distance((ti[0].centerx, ti[0].centery), (self.rect.centerx, self.rect.centery)) / (self.vel / 1.5) < tile_s:
                    self.walls.append(ti)
            self.sample_counter = 0

    def blit(self, s):
        pygame.draw.circle(s, self.color2, (self.rect.centerx + self.size / 4, self.rect.centery + self.size / 4), self.size)
        pygame.draw.circle(s, self.color, (self.rect.centerx, self.rect.centery), self.size)

    def move(self, delta_t):
        self.rect.x += self.vel * math.cos(self.a) * delta_t * self.dir[0]
        for w in self.walls:
            if w[0].colliderect(self.rect):
                if math.cos(self.a) * self.dir[0] > 0:
                    self.dir[0] *= -1
                    self.rect.right = (w[0].left - self.vel)
                    self.vel *= self.bounciness
                elif math.cos(self.a) * self.dir[0] < 0:
                    self.dir[0] *= -1
                    self.rect.left = (w[0].right + self.vel)
                    self.vel *= self.bounciness
        self.rect.y += self.vel * math.sin(self.a) * delta_t * self.dir[1]
        for w in self.walls:
            if w[0].colliderect(self.rect):
                if math.sin(self.a) * self.dir[1] > 0:
                    self.dir[1] *= -1
                    self.rect.bottom = (w[0].top - self.vel)
                    self.vel *= self.bounciness
                elif math.sin(self.a) * self.dir[1] < 0:
                    self.dir[1] *= -1
                    self.rect.top = (w[0].bottom + self.vel)
                    self.vel *= self.bounciness
        if self.timer <= 0:
            return True


class bullet:
    # This initializes the bullet object with its parameters
    def __init__(self, rect, bx, by, x_vel, y_vel, ang, ricochet, col, dmg, b_timer):
        self.rect = rect
        self.x = bx
        self.y = by
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.angle = ang
        self.ric = ricochet
        self.col = col
        self.dmg = dmg
        self.timer = b_timer

    def collide(self, tiles):
        for ti in tiles:
            if ti.colliderect(self.rect):
                if math.fabs(ti.top - self.y - self.rect.height) < (tile_size / 3):
                    self.y = ti.top - 5 - self.rect.height
                    self.y_vel *= -1
                    self.ric -= 1
                if math.fabs(ti.bottom - self.y) < (tile_size / 3):
                    self.y = ti.bottom + 5
                    self.y_vel *= -1
                    self.ric -= 1
            if ti.colliderect(self.rect):
                if math.fabs(ti.left - self.x - self.rect.width) < (tile_size / 3):
                    self.x = ti.left - 5 - self.rect.width
                    self.x_vel *= -1
                    self.ric -= 1
                if math.fabs(ti.right - self.rect.left) < (tile_size / 3):
                    self.x = ti.right + 5
                    self.x_vel *= -1
                    self.ric -= 1
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        self.x += self.x_vel * self.angle[0]
        self.y += self.y_vel * self.angle[1]


class spark:
    # This function initializes the spark object by taking in parameters
    def __init__(self, sx, sy, vel, color, color2, size, angle, decay, speed_decay, rotation, gravity, length):
        self.x = sx
        self.y = sy
        self.vel = vel
        self.color = color
        self.color2 = color2
        self.size = size
        self.angle = angle
        self.decay = decay
        self.gravity = gravity
        self.rotation = rotation
        self.speed_decay = speed_decay
        self.length = length

    # This function is used for creating the vertices of the spark, in the shape of a diamond, using parameters given
    # when the object was initialized such as the x, y, size, length, and angle
    # This function then uses those points to draw the polygon on the screen
    # The function also draws a shadow below the diamond using the points and the "shadow" parameter
    def blit(self, s, shifted_scroll):
        points = [(self.x + (self.size * self.length/3 * math.cos(self.angle)) - self.size - shifted_scroll[0], self.y + (self.size * 2 * math.sin(self.angle)) + self.size - shifted_scroll[1]),
                  (self.x + (self.size * math.cos(self.angle + math.pi / 2)) - self.size - shifted_scroll[0], self.y + (self.size * math.sin(self.angle + math.pi / 2)) + self.size - shifted_scroll[1]),
                  (self.x + (self.size * 2 * self.length/3 * math.cos(self.angle + math.pi)) - self.size - shifted_scroll[0], self.y + (self.size * 3 * math.sin(self.angle + math.pi)) + self.size - shifted_scroll[1]),
                  (self.x + (self.size * math.cos(self.angle - math.pi / 2)) - self.size - shifted_scroll[0], self.y + (self.size * math.sin(self.angle - math.pi / 2)) + self.size - shifted_scroll[1])]
        pygame.draw.polygon(s, self.color2, points)
        points = [(self.x + (self.size * self.length/3 * math.cos(self.angle)) - shifted_scroll[0], self.y + (self.size * 2 * math.sin(self.angle)) - shifted_scroll[1]),
                  (self.x + (self.size * math.cos(self.angle + math.pi / 2)) - shifted_scroll[0], self.y + (self.size * math.sin(self.angle + math.pi/2)) - shifted_scroll[1]),
                  (self.x + (self.size * 2 * self.length/3 * math.cos(self.angle + math.pi)) - shifted_scroll[0], self.y + (self.size * 3 * math.sin(self.angle + math.pi)) - shifted_scroll[1]),
                  (self.x + (self.size * math.cos(self.angle - math.pi / 2)) - shifted_scroll[0], self.y + (self.size * math.sin(self.angle - math.pi/2)) - shifted_scroll[1])]
        pygame.draw.polygon(s, self.color, points)

    # This function uses the angle, decay, gravity, rotation, and speed_decay parameters to move the points
    def move(self, t):
        self.x += self.vel * math.cos(self.angle) * t
        self.y += self.gravity * t
        self.y += self.vel * math.sin(self.angle) * t
        self.size -= self.decay * t
        self.rotation = 1 / (self.size * 20)
        if self.vel > 0:
            self.vel -= self.speed_decay * t
        if 3 * math.pi / 2 > self.angle > math.pi / 2:
            self.angle -= self.rotation * t
        if 5 * math.pi / 2 > self.angle > 3 * math.pi / 2:
            self.angle += self.rotation * t
        if math.pi / 2 > self.angle > 0:
            self.angle += self.rotation * t

