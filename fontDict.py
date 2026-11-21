import os
import pygame

pygame.init()

styles = ["regular", "bold", "thin", "extralight"]
sizes = [i for i in range(100)]

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


class Fonts(dict):
    def __missing__(self, key):
        style = key.rstrip("0123456789")
        size = int(key[len(style):])
        path = os.path.join(folder, f"Montserrat-{style.capitalize()}.ttf")
        self[key] = pygame.font.Font(path, size)
        return self[key]


fonts = Fonts()
