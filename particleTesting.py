import pygame
import math
import time
import random
from text import draw_text
from particles import Torch

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
pygame.font.get_fonts()
font15 = pygame.font.Font("freesansbold.ttf", 15)
font20 = pygame.font.Font("freesansbold.ttf", 20)
font30 = pygame.font.Font("freesansbold.ttf", 30)
font40 = pygame.font.Font("freesansbold.ttf", 40)
better_font20 = pygame.font.SysFont("keyboard.ttf", 20)
better_font30 = pygame.font.SysFont("keyboard.ttf", 30)
better_font40 = pygame.font.SysFont("keyboard.ttf", 40)
better_font_adaptive = pygame.font.SysFont("keyboard.ttf", int(40 / (scaleDownFactor ** (1 / 1.5))))
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
    greyVVDB = [20, 25, 30]
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


# Defining some more variables to use in the game loop
oscillating_random_thing = 0
ShakeCounter = 0
toggle = True
click = False

torchImg = pygame.image.load("torchImg.png").convert_alpha()
torchSur = pygame.Surface((20, 32), pygame.SRCALPHA)
torchSur.blit(torchImg, (0, 0))
torch = Torch(screen_center[0] / scaleDownFactor, screen_center[1] / scaleDownFactor, FireCols.cols[0:5], FireCols.colsReversed, FireCols.colsReversed)

# ---------------- Main Game Loop
last_time = time.time()
running = True
while running:

    # ---------------- Reset Variables and Clear screens
    mx, my = pygame.mouse.get_pos()
    mx, my = mx / scaleDownFactor, my / scaleDownFactor
    screen.fill(Endesga.greyVVDB)
    screen2.fill(Endesga.greyVVDB)
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

    torch.update(dt)
    torch.spawn()
    screen2.blit(torchSur, (torch.x - 10, torch.y + 2))
    torch.draw(screen2, (0, 0))

    # ---------------- Updating Screen
    if toggle:
        items = {round(clock.get_fps()): None,
                 }
        for i, label in enumerate(items.keys()):
            string = str(label)
            if items[label] is not None:
                string = f"{items[label]}: " + string
            draw_text(screenUI, Endesga.debug_red, better_font_adaptive, 5, screen_height / scaleDownFactor - (30 + 30 * i) / (scaleDownFactor ** (1 / 1.5)), string, Endesga.black, int(3 / scaleDownFactor) + int(3 / scaleDownFactor) < 1, antiAliasing=False)
        pygame.mouse.set_visible(False)
        pygame.draw.circle(screenUI, Endesga.black, (mx + 1, my + 1), 2, 1)
        pygame.draw.circle(screenUI, Endesga.white, (mx, my), 2, 1)
    screen.blit(pygame.transform.scale(screen2, (screen_width, screen_height)), (shake[0], shake[1]))
    screen.blit(pygame.transform.scale(screenT, (screen_width, screen_height)), (shake[0], shake[1]))
    screen.blit(pygame.transform.scale(screenUI, (screen_width, screen_height)), (0, 0))
    pygame.display.update()
    clock.tick(fps)
