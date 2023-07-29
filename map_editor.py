import pygame
import math
import time
from calcs import distance
from text import draw_text

pygame.init()

# ---------------- Setting up the screen, assigning some global variables, and loading text fonts
screen = pygame.display.set_mode((1050, 700))
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
scroll = [0, 0]
scrolling = [0, 0]
scrolling_speed = 10
shake_strength = 3
pygame.font.get_fonts()
font15 = pygame.font.Font("freesansbold.ttf", 15)
font20 = pygame.font.Font("freesansbold.ttf", 20)
font30 = pygame.font.Font("freesansbold.ttf", 30)
font40 = pygame.font.Font("freesansbold.ttf", 40)
better_font40 = pygame.font.SysFont("keyboard.ttf", 40)
font50 = pygame.font.Font("freesansbold.ttf", 50)
font100 = pygame.font.Font("freesansbold.ttf", 100)


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
    debug_red = (255, 96, 141)
    sebastian_lague_purple = (70, 74, 124)
    sebastian_lague_light_purple = [137, 133, 181]


# ---------------- Processing previous map
unprocessed_data = []
full_list = []
sorted_list = []
file = 'layout2.txt'
with open(file, 'r') as f:
    lines = f.readlines()
    for li in lines:
        unprocessed_data.append(li.strip("\n"))

for line in unprocessed_data:
    for char in line:
        full_list.append(int(char))

temp = []
for i, char in enumerate(full_list):
    temp.append(char)
    if (i + 1) % len(unprocessed_data[0]) == 0:
        sorted_list.append(temp)
        temp = []


class Tiles:
    def __init__(self, tile_type, color, num, shadow):
        self.type = tile_type
        self.col = color
        self.rect = pygame.rect.Rect(0, 0, 0, 0)
        self.num = num
        self.shadow = shadow


tile_types = [Tiles("Clear", (255, 50, 100), 0, False), Tiles('Wall', (245, 240, 245), 1, True), Tiles('Water', (10, 80, 120), 2, False)]
UI_size = 50
for i, ti in enumerate(tile_types):
    ti.rect = pygame.rect.Rect((screen_width / 2 - (len(tile_types) - (i + 1)) * UI_size), screen_height - UI_size * 1.3, UI_size, UI_size)
UI_rect = pygame.rect.Rect((screen_width / 2 - (len(tile_types) - 1) * UI_size) - UI_size * 0.25, screen_height - UI_size * 1.4, UI_size * len(tile_types) + UI_size * 0.5, UI_size * 1.2)


def create_rect(tile_, tile_x, tile_y, ts, tile_type_nums, lists):
    for t_i, til in enumerate(tile_type_nums):
        if tile_ == tile_type_nums[t_i]:
            lists[t_i].append(pygame.rect.Rect(tile_size * tile_x, tile_size * tile_y, tile_size, ts))
    return lists


tile_size = 9
tile_rects = []
water_rects = []
all_rects = []
ty = 0
print(len(sorted_list[0]), len(sorted_list))
for row in sorted_list:
    tx = 0
    for tile in row:
        all_rects.append(pygame.rect.Rect(tile_size * tx, tile_size * ty, tile_size, tile_size))
        tile_rects, water_rects = create_rect(tile, tx, ty, tile_size, [1, 2], [tile_rects, water_rects])
        tx += 1
    ty += 1


# Defining some more variables to use in the game loop
oscillating_random_thing = 0
ShakeCounter = 0
click = False
selected_block = 1
brush_size = 0.5
# ---------------- Main Game Loop
last_time = time.time()
running = True
while running:

    # ---------------- Reset Variables and Clear screens
    oscillating_random_thing += math.pi/fps
    mx, my = pygame.mouse.get_pos()
    screen.fill(Endesga.my_blue)
    screen2.fill(Endesga.my_blue)
    screenT.fill((0, 0, 0, 0))
    screenUI.fill((0, 0, 0, 0))
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    timer -= 1 * dt
    shake = [0, 0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                write_lines = []
                temp = ''
                for i, char in enumerate(full_list):
                    temp += str(char)
                    if (i + 1) % len(unprocessed_data[0]) == 0:
                        write_lines.append(temp + '\n')
                        temp = ''
                with open(file, 'w') as f:
                    f.writelines(write_lines)
                running = False
            if event.key == pygame.K_RIGHT:
                scrolling[0] += scrolling_speed
            if event.key == pygame.K_LEFT:
                scrolling[0] -= scrolling_speed
            if event.key == pygame.K_UP:
                scrolling[1] -= scrolling_speed
            if event.key == pygame.K_DOWN:
                scrolling[1] += scrolling_speed
            if event.key == pygame.K_d:
                scrolling[0] += scrolling_speed
            if event.key == pygame.K_a:
                scrolling[0] -= scrolling_speed
            if event.key == pygame.K_w:
                scrolling[1] -= scrolling_speed
            if event.key == pygame.K_s:
                scrolling[1] += scrolling_speed
            if event.key == pygame.K_1:
                brush_size = 0.5
            if event.key == pygame.K_2:
                brush_size = 1.5
            if event.key == pygame.K_3:
                brush_size = 2.5
            if event.key == pygame.K_4:
                brush_size = 3.5
            if event.key == pygame.K_5:
                brush_size = 4.5
            if event.key == pygame.K_6:
                brush_size = 5.5
            if event.key == pygame.K_7:
                brush_size = 6.5
            if event.key == pygame.K_8:
                brush_size = 7.5
            if event.key == pygame.K_9:
                brush_size = 8.5
            if event.key == pygame.K_0:
                brush_size = 19.5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                scrolling[0] -= scrolling_speed
            if event.key == pygame.K_LEFT:
                scrolling[0] += scrolling_speed
            if event.key == pygame.K_UP:
                scrolling[1] += scrolling_speed
            if event.key == pygame.K_DOWN:
                scrolling[1] -= scrolling_speed
            if event.key == pygame.K_d:
                scrolling[0] -= scrolling_speed
            if event.key == pygame.K_a:
                scrolling[0] += scrolling_speed
            if event.key == pygame.K_w:
                scrolling[1] += scrolling_speed
            if event.key == pygame.K_s:
                scrolling[1] -= scrolling_speed

    scroll[0] += scrolling[0]
    scroll[1] += scrolling[1]

    for t in tile_rects:
        pygame.draw.rect(screen2, Endesga.greyL, (t.x - t.width / 7 - scroll[0], t.y + t.height / 7 - scroll[1], t.width, t.height))

    for t in tile_rects:
        pygame.draw.rect(screen2, Endesga.white, (t.x - scroll[0], t.y - scroll[1], t.width, t.height))

    for w in water_rects:
        pygame.draw.rect(screen2, (10, 80, 120), (w.x - scroll[0], w.y - scroll[1], w.width, w.height))

    tile_rects = []
    water_rects = []
    ty = 0
    for row in sorted_list:
        tx = 0
        for tile in row:
            tile_rects, water_rects = create_rect(tile, tx, ty, tile_size, [1, 2], [tile_rects, water_rects])
            tx += 1
        ty += 1

    for i, t in enumerate(all_rects):
        if click:
            if distance((t.centerx, t.centery), (mx + scroll[0], my + scroll[1])) < (brush_size * tile_size) and not UI_rect.collidepoint((mx, my)):
                full_list[i] = selected_block
                sorted_list[i//(len(unprocessed_data[0]))][i % len(unprocessed_data[0])] = selected_block
        # Light - i % 89 == 79 or i % 76 == 57 or i % 86 == 33
        # Dense - i % 17 == 5 or i % 29 == 7 or i % 31 == 11 or i % 37 == 17 or i % 41 == 19 or i % 59 == 23 or i % 73 == 29
        if i % 89 == 79 or i % 76 == 57 or i % 86 == 33:
            pygame.draw.rect(screen2, Endesga.greyL, (t.x - scroll[0], t.y - scroll[1], t.width, t.height), 1)

    # ---------------- Blitting and detecting clicks for UI
    pygame.draw.rect(screenUI, Endesga.greyVD, UI_rect, 0, int(UI_size / 16))
    for i, tt in enumerate(tile_types):
        if tt.type == "Clear":
            pygame.draw.rect(screenUI, (179, 36, 71), tt.rect, 0, int(UI_size / 8))
            pygame.draw.circle(screenUI, tt.col, tt.rect.center, tt.rect.width / 2.2, 6)
            pygame.draw.line(screenUI, tt.col, (tt.rect.centerx - tt.rect.width / 4.4, tt.rect.centery - tt.rect.height / 4.4),
                             (tt.rect.centerx + tt.rect.width / 4.4, tt.rect.centery + tt.rect.height / 4.4), 10)
        else:
            pygame.draw.rect(screenUI, tt.col, tt.rect, 0, int(UI_size / 8))
        if tt.rect.collidepoint((mx, my)):
            if click:
                selected_block = tt.num

    # ---------------- Updating Screen
    draw_text(screen2, Endesga.debug_red, Endesga.black, better_font40, 20, screen_height - 40, False, str(int(mx)) + ", " + str(int(my)), 3, False, None)
    pygame.mouse.set_visible(False)
    pygame.draw.circle(screenUI, Endesga.greyL, (mx, my), 2)
    pygame.draw.circle(screenUI, Endesga.greyL, (mx, my), brush_size * tile_size, 1)
    screen.blit(screen2, (shake[0], shake[1]))
    screen.blit(screenT, (0, 0))
    screen.blit(screenUI, (0, 0))
    pygame.display.update()
    clock.tick(fps)
