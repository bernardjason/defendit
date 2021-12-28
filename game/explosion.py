import random

import game
from game.landscape import Landscape


class Explosion:
    particles: list = []

    colours = ["red", "orange", "pink", "yellow", "cyan"]

    @staticmethod
    def create(x, y):
        for i in range(1, random.randint(10, 20)):
            e = Explosion(x, y)
            Explosion.particles.append(e)

    @staticmethod
    def render(delta):
        for e in Explosion.particles:
            display, screen_x, screen_y = Landscape.map_to_screen(e.x, e.y)

            game.runtime.main_canvas.create_rectangle(screen_x, screen_y,
                                                      screen_x + 7, screen_y + 7, fill=Explosion.colours[e.colour])
            e.x = e.x + e.direction_x
            e.y = e.y + e.direction_y
            e.clicks = e.clicks - 1 * delta
            if e.clicks < 0:
                Explosion.particles.remove(e)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction_x = random.randint(-1000, 1000) / 1000
        self.direction_y = random.randint(-1000, 1000) / 1000
        self.clicks = random.randint(30, 120)
        self.colour = random.randint(0, len(Explosion.colours) - 1)
