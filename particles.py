import pygame
import math
from calcs import distance
from calcs import normalize_angle
from calcs import brightness
import random


class Shockwave:
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


class Particle:
    # Function for initializing the particle object with its parameters
    def __init__(self, px, py, x_vel, y_vel, color, color2, size, decay, gravity, bounciness):
        self.x = px
        self.y = py
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.color2 = color2
        self.size = size
        self.decay = decay
        self.gravity = gravity
        self.bounciness = bounciness

    # Function for drawing the particle on the screen
    def blit(self, s):
        pygame.draw.circle(s, self.color2, (self.x - self.size / 4, self.y + self.size / 4), self.size)
        pygame.draw.circle(s, self.color, (self.x, self.y), self.size)

    # Function that is called every frame for moving the particle
    def move(self, dt):
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt
        self.y_vel += self.gravity * dt
        self.size -= self.decay * dt


class bullet:
    # This initializes the bullet object with its parameters
    def __init__(self, r, x, y, vel, angle, ricochet, col, dmg, t):
        self.r = r
        self.rect = pygame.rect.Rect(x - self.r, y - self.r, self.r * 2, self.r * 2)
        self.vel = vel
        self.a = normalize_angle(angle)
        self.ric = ricochet
        self.has_bounced = False
        self.col = col
        self.dmg = dmg
        self.sample_counter = 0
        self.sample_rate = 2
        self.walls = []
        self.movement = [1, 0]
        self.dir = [1, 1]
        self.timer = t * 60

    def update(self, ts, tile_s, delta_t):
        self.has_bounced = False
        self.timer -= 1 * delta_t
        self.sample_counter += 1
        if self.sample_counter > self.sample_rate:
            self.walls = []
            for ti in ts:
                if distance((ti[0].centerx, ti[0].centery), (self.rect.centerx, self.rect.centery)) / (self.vel / 1.5) < tile_s:
                    self.walls.append(ti)
            self.sample_counter = 0

    def move(self, delta_t):
        if self.movement[0] == 1:
            self.rect.x += self.vel * math.cos(self.a) * delta_t * self.dir[0]
            for w in self.walls:
                if w[0].colliderect(self.rect):
                    if not self.has_bounced:
                        self.ric -= 1
                        self.has_bounced = True
                    if math.cos(self.a) * self.dir[0] > 0:
                        self.dir[0] *= -1
                        self.rect.right = (w[0].left - self.vel)
                    elif math.cos(self.a) * self.dir[0] < 0:
                        self.dir[0] *= -1
                        self.rect.left = (w[0].right + self.vel)
            self.rect.y += self.vel * math.sin(self.a) * delta_t * self.dir[1]
            for w in self.walls:
                if w[0].colliderect(self.rect):
                    if not self.has_bounced:
                        self.ric -= 1
                        self.has_bounced = True
                    if math.sin(self.a) * self.dir[1] > 0:
                        self.dir[1] *= -1
                        self.rect.bottom = (w[0].top - self.vel)
                    elif math.sin(self.a) * self.dir[1] < 0:
                        self.dir[1] *= -1
                        self.rect.top = (w[0].bottom + self.vel)
        if self.ric < 0 or self.timer <= 0:
            return True

    def draw(self, s, scr, show_rects, show_hitbox):
        if show_rects:
            for w in self.walls:
                pygame.draw.rect(s, (200, 100, 100), (w[0].x - scr[0], w[0].y - scr[1], w[0].w, w[0].h))
        if show_hitbox:
            pygame.draw.rect(s, self.col, (self.rect.x - scr[0], self.rect.y - scr[1], self.rect.w, self.rect.h), 1)
        pygame.draw.circle(s, self.col, (self.rect.centerx - scr[0], self.rect.centery - scr[1]), self.r)


class Glow:
    # Function for initializing the particle object with its parameters
    def __init__(self, px, py, x_vel, y_vel, color, color2, glow_col, size, min_size, decay, gravity, flicker):
        self.x = px
        self.y = py
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.color2 = color2
        self.glow_col = glow_col
        self.size = size
        self.min_size = min_size
        self.decay = decay
        self.gravity = gravity
        self.offset = random.uniform(0, 2 * math.pi)
        self.flicker = flicker

    # Function for drawing the particle on the screen
    def blit(self, s, oscillating_thing):
        if self.color2 is not None:
            pygame.draw.circle(s, self.color2, (self.x - self.size / 4, self.y + self.size / 4), self.size)
        pygame.draw.circle(s, self.color, (self.x, self.y), self.size)

        surf = pygame.Surface((self.size * 4 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker * 2, self.size * 4 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker * 2))
        if self.glow_col is None:
            pygame.draw.circle(surf, brightness(self.color, 0.1), (self.size * 2 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker, self.size * 2 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker), self.size * 2 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker)
        else:
            pygame.draw.circle(surf, self.glow_col, (self.size * 2 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker, self.size * 2 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker), self.size * 2 + (math.sin(oscillating_thing + self.offset) + 1) * self.flicker)
        surf.set_colorkey((0, 0, 0))
        s.blit(surf, (self.x - self.size * 2 - (math.sin(oscillating_thing + self.offset) + 1) * self.flicker, self.y - self.size * 2 - (math.sin(oscillating_thing + self.offset) + 1) * self.flicker), special_flags=pygame.BLEND_RGB_ADD)

    # Function that is called every frame for moving the particle
    def move(self, dt):
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt
        self.y_vel += self.gravity * dt
        self.size -= self.decay * dt
        if self.size < self.min_size:
            return True


class Spark:
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
