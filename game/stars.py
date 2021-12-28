import random

import game
from game.landscape import Landscape


class Stars:
    particles: list = []

    colours = ["blue", "purple", "pink", "yellow", "black", "magenta"]

    @staticmethod
    def create():
        for x in range(0, Landscape.LANDSCAPE_MAX * Landscape.SCALE, 50):
            if random.randint(0, 10) < 3:
                y = random.randint(100, game.SCREEN_Y - 100)
                for i in range(1, random.randint(10, 20)):
                    e = Stars(x, y)
                    Stars.particles.append(e)

    @staticmethod
    def render():
        for e in Stars.particles:
            display, screen_x, screen_y = Landscape.map_to_screen(e.x, e.y)

            if display:
                e.twinkle = e.twinkle - 1
                game.runtime.main_canvas.create_rectangle(screen_x, screen_y,
                                                          screen_x + 4, screen_y + 4, fill=Stars.colours[e.colour])
                if e.twinkle <= 0:
                    e.twinkle = random.randint(50, 100)
                    e.colour = (e.colour + 1) % len(Stars.colours)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = random.randint(0, len(Stars.colours) - 1)
        self.twinkle = random.randint(0, 200)
