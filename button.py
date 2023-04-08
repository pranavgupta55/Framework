import pygame


def create_buttons(num_hor, num_ver, space_hor, space_ver, width, height, text, clicked, coord):
    timer = []
    buttons_list = []
    text_list = []
    color_list = []
    for i in range(num_hor):
        for o in range(num_ver):
            buttons_list.append(pygame.Rect(coord[0] + (width + space_hor) * i, coord[1] + (height + space_ver) * o, width, height))
            clicked.append(False)
    for i in range(num_hor * num_ver):
        text_list.append(text[i])
    for i in range(num_hor * num_ver):
        timer.append(0)
    return [buttons_list, text_list, clicked, color_list, timer]


def draw_buttons(button_rect_list, button_text_list, button_clicked_list, color_list, timer_list, screen, border_width, corner_radius, font, c, mX, mY):
    for i, b in enumerate(button_rect_list):
        button_text = button_text_list[i]
        button_color = color_list[0]
        text_color = color_list[1]
        text_length, text_height = pygame.font.Font.size(font, button_text)
        text_pos = button_rect_list[i].x + button_rect_list[i].width / 2 - text_length / 2, button_rect_list[i].y + button_rect_list[i].height / 2 - text_height / 2
        if pygame.Rect.collidepoint(button_rect_list[i], (mX, mY)):
            button_color = color_list[2]
            if c:
                button_clicked_list[i] = True
                timer_list[i] = 10
        else:
            button_clicked_list[i] = False
        if timer_list[i] > 0:
            button_color = color_list[3]
            timer_list[i] -= 1
        pygame.draw.rect(screen, button_color, button_rect_list[i], border_width, corner_radius)
        screen.blit(font.render(button_text, True, text_color), text_pos)
