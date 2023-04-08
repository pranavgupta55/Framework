import pygame


def draw_text(screen_, color_, color2_, font_, x_, y_, centered_, text_, shadow_size_):
    if centered_:
        screen_.blit(font_.render(text_, True, color2_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2 + shadow_size_, y_ + shadow_size_))
        screen_.blit(font_.render(text_, True, color_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2, y_))
    else:
        screen_.blit(font_.render(text_, True, color2_), (x_ + shadow_size_, y_ + shadow_size_))
        screen_.blit(font_.render(text_, True, color_), (x_, y_))
