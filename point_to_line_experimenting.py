import pygame
import math
import time
import random
from text import draw_text
from text import simpleText
from calcs import collide_circle
from calcs import point_to_line

pygame.init()

# ---------------- Setting up the screen, assigning some global variables, and loading text fonts
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60
screen_width = screen.get_width()
screen_height = screen.get_height()
screen2 = pygame.Surface((screen_width, screen_height)).convert_alpha()
screenT = pygame.Surface((screen_width, screen_height)).convert_alpha()
screenT.set_alpha(100)
screenUI = pygame.Surface((screen_width, screen_height)).convert_alpha()
timer = 0
shake = [0, 0]
shake_strength = 3
scroll = [0, 0]
pygame.font.get_fonts()
font15 = pygame.font.Font("freesansbold.ttf", 15)
font20 = pygame.font.Font("freesansbold.ttf", 20)
font30 = pygame.font.Font("freesansbold.ttf", 30)
font40 = pygame.font.Font("freesansbold.ttf", 40)
better_font40 = pygame.font.SysFont("keyboard.ttf", 40)
font50 = pygame.font.Font("freesansbold.ttf", 50)
font100 = pygame.font.Font("freesansbold.ttf", 100)


class Endesga:
    maroon_red = [87, 28, 39]
    lighter_maroon_red = [127, 36, 51]
    dark_green = [9, 26, 23]
    light_brown = [191, 111, 74]
    black = [19, 19, 19]
    grey_blue = [66, 76, 110]
    cream = [237, 171, 80]
    white = [255, 255, 255]
    greyL = [200, 200, 200]
    grey = [150, 150, 150]
    greyD = [100, 100, 100]
    greyVD = [50, 50, 50]
    very_light_blue = [199, 207, 221]
    my_blue = [32, 36, 46]
    debug_red = [255, 96, 141]
    sebastian_lague_purple = [70, 74, 124]
    sebastian_lague_light_purple = [137, 133, 181]


# Defining some more variables to use in the game loop
oscillating_random_thing = 0
ShakeCounter = 0
click = False
closest = [0, 0]
dist = screen_width
pairs = []
buffer = 200
point_size = 5

for i in range(5):
    pairs.append([[random.randint(buffer, screen_width - buffer), random.randint(buffer, screen_height - buffer)],
                  [random.randint(buffer, screen_width - buffer), random.randint(buffer, screen_height - buffer)]])


# ---------------- Main Game Loop
last_time = time.time()
running = True
while running:

    # ---------------- Reset Variables and Clear screens
    mx, my = pygame.mouse.get_pos()
    screen.fill(Endesga.my_blue)
    screen2.fill(Endesga.my_blue)
    screenT.fill((0, 0, 0, 0))
    screenUI.fill((0, 0, 0, 0))
    dt = time.time() - last_time
    dt *= fps
    last_time = time.time()
    timer -= 1 * dt
    shake = [0, 0]
    oscillating_random_thing += math.pi / fps * dt
    dist = screen_width

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            pass

    for i, pair in enumerate(pairs):
        pygame.draw.line(screen2, Endesga.white, pairs[i][0], pairs[i][1])

    for i, pair in enumerate(pairs):
        for p in pair:
            pygame.draw.circle(screen2, Endesga.debug_red, p, point_size)
            if collide_circle(p, (mx, my), point_size * 1.5):
                simpleText(screenUI, Endesga.white, better_font40, p[0], p[1], str(p))

    for pair in pairs:
        if point_to_line((mx, my), pair)[0] < dist:
            dist, closest = point_to_line((mx, my), pair)
    pygame.draw.circle(screen2, Endesga.white, closest, point_size * 2)

    # ---------------- Updating Screen
    simpleText(screen2, Endesga.white, better_font40, 20, screen_height - 40, f"Distance to nearest line: {int(dist)}")
    pygame.mouse.set_visible(False)
    pygame.draw.circle(screenUI, Endesga.white, (mx, my), 5, 1)
    screen.blit(screen2, (shake[0], shake[1]))
    screen.blit(screenT, (0, 0))
    screen.blit(screenUI, (0, 0))
    pygame.display.update()
    clock.tick(fps)
