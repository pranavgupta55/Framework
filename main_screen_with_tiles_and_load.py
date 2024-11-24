import pygame
import math
import time
import random
from text import draw_text
from fontDict import fonts

pygame.init()

# ---------------- Setting up the screen, assigning some global variables, and loading text fonts
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60
screen_width = screen.get_width()
screen_height = screen.get_height()
scaleDownFactor = 3
screen_center = [screen_width / 2, screen_height / 2]
screen2 = pygame.Surface((screen_width / scaleDownFactor, screen_height / scaleDownFactor)).convert_alpha()
screenT = pygame.Surface((screen_width / scaleDownFactor, screen_height / scaleDownFactor)).convert_alpha()
screenT.set_alpha(100)
screenUI = pygame.Surface((screen_width / scaleDownFactor, screen_height / scaleDownFactor)).convert_alpha()
timer = 0
shake = [0, 0]
shake_strength = 3
montserratRegularAdaptive = fonts[f"regular{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
montserratExtralightAdaptive = fonts[f"extralight{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
montserratBoldAdaptive = fonts[f"bold{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
montserratThinAdaptive = fonts[f"thin{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]


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
    network_green = [64, 128, 67]
    network_red = [127, 45, 41]


class FireCols:
    cols = [[255, 242, 157], [255, 212, 124], [255, 169, 70], [254, 128, 3], [230, 106, 37], [179, 46, 19], [126, 19, 6], [70, 2, 14]]
    colsReversed = [[70, 2, 14], [126, 19, 6], [179, 46, 19], [230, 106, 37], [254, 128, 3], [255, 169, 70], [255, 212, 124], [255, 242, 157]]


unprocessed_data = []
full_list = []
sorted_list = []
with open('layout.txt') as f:
    lines = f.readlines()
    for li in lines:
        unprocessed_data.append(li.strip("\n"))

for li in unprocessed_data:
    for char in li:
        full_list.append(int(char))

temp = []
for i, char in enumerate(full_list):
    temp.append(char)
    if (i + 1) % len(unprocessed_data[0]) == 0:
        sorted_list.append(temp)
        temp = []

tile_size = int(30 / scaleDownFactor)
tile_rects = []
ty = 0
for row in sorted_list:
    tx = 0
    for tile in row:
        if tile == 1:
            tile_rects.append(pygame.rect.Rect(tile_size * tx, tile_size * ty, tile_size, tile_size))
        tx += 1
    ty += 1

# Defining some more variables to use in the game loop
oscillating_random_thing = 0
ShakeCounter = 0
toggle = True
click = False

# ---------------- Main Game Loop
last_time = time.time()
running = True
while running:

    # ---------------- Reset Variables and Clear screens
    mx, my = pygame.mouse.get_pos()
    mx, my = mx / scaleDownFactor, my / scaleDownFactor
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
            if event.key == pygame.K_SPACE:
                toggle = not toggle
        if event.type == pygame.KEYUP:
            pass

    for t in tile_rects:
        pygame.draw.rect(screen2, Endesga.greyL, (t.x - t.width / 6, t.y + t.height / 4, t.width, t.height))

    for t in tile_rects:
        pygame.draw.rect(screen2, Endesga.white, t)

    # ---------------- Updating Screen
    if toggle:
        items = {round(clock.get_fps()): None,
                 }
        for i, label in enumerate(items.keys()):
            string = str(label)
            if items[label] is not None:
                string = f"{items[label]}: " + string
            draw_text(screenUI, Endesga.debug_red, montserratRegularAdaptive, 5, screen_height / scaleDownFactor - (30 + 25 * i) / (scaleDownFactor ** (1 / 1.8)), string, Endesga.black, int(3 / scaleDownFactor) + int(3 / scaleDownFactor) < 1, antiAliasing=False)
        pygame.mouse.set_visible(False)
        pygame.draw.circle(screenUI, Endesga.black, (mx + 1, my + 1), 2, 1)
        pygame.draw.circle(screenUI, Endesga.white, (mx, my), 2, 1)
    screen.blit(pygame.transform.scale(screen2, (screen_width, screen_height)), (shake[0], shake[1]))
    screen.blit(pygame.transform.scale(screenT, (screen_width, screen_height)), (shake[0], shake[1]))
    screen.blit(pygame.transform.scale(screenUI, (screen_width, screen_height)), (0, 0))
    pygame.display.update()
    clock.tick(fps)
