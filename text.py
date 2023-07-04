import pygame


def draw_text(screen_, color_, color2_, font_, x_, y_, centered_, text_, shadow_size_, wrap_, max_len):
    if wrap_:
        if pygame.font.Font.size(font_, text_)[0] > max_len:
            all_words = []
            temp = ""
            complete_row = ""
            output = []
            for i, char in enumerate(text_):
                if char != " ":
                    temp += char
                else:
                    all_words.append(temp + " ")
                    temp = ""
                if i + 1 == len(text_):
                    all_words.append(temp)
            for i, word in enumerate(all_words):
                if pygame.font.Font.size(font_, word)[0] + pygame.font.Font.size(font_, complete_row)[0] > max_len:
                    output.append(complete_row)
                    complete_row = "" + word
                else:
                    complete_row += word
            output.append(complete_row)
            if centered_:
                for i, row in enumerate(output):
                    screen_.blit(font_.render(row, True, color2_), (x_ - pygame.font.Font.size(font_, row)[0] / 2 + shadow_size_, y_ + shadow_size_ + ((i - len(output) / 2) * 1.1 * pygame.font.Font.size(font_, row)[1])))
                    screen_.blit(font_.render(row, True, color_), (x_ - pygame.font.Font.size(font_, row)[0] / 2, y_ + ((i - len(output) / 2) * 1.1 * pygame.font.Font.size(font_, row)[1])))
            else:
                for i, row in enumerate(output):
                    screen_.blit(font_.render(row, True, color2_), (x_ + shadow_size_, y_ + shadow_size_ + (i * 1.1 * pygame.font.Font.size(font_, row)[1])))
                    screen_.blit(font_.render(row, True, color_), (x_, y_ + (i * 1.1 * pygame.font.Font.size(font_, row)[1])))
        else:
            if centered_:
                screen_.blit(font_.render(text_, True, color2_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2 + shadow_size_, y_ - pygame.font.Font.size(font_, text_)[1] / 2 + shadow_size_))
                screen_.blit(font_.render(text_, True, color_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2, y_ - pygame.font.Font.size(font_, text_)[1] / 2))
            else:
                screen_.blit(font_.render(text_, True, color2_), (x_ + shadow_size_, y_ + shadow_size_))
                screen_.blit(font_.render(text_, True, color_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2, y_))
    else:
        if centered_:
            screen_.blit(font_.render(text_, True, color2_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2 + shadow_size_, y_ - pygame.font.Font.size(font_, text_)[1] / 2 + shadow_size_))
            screen_.blit(font_.render(text_, True, color_), (x_ - pygame.font.Font.size(font_, text_)[0] / 2, y_ - pygame.font.Font.size(font_, text_)[1] / 2))
        else:
            screen_.blit(font_.render(text_, True, color2_), (x_ + shadow_size_, y_ + shadow_size_))
            screen_.blit(font_.render(text_, True, color_), (x_, y_))
