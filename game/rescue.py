import random

from PIL import Image, ImageTk

import game
from game.landscape import Landscape


class Rescue:
    WIDTH = 16
    HEIGHT = 32
    png = None
    img = None
    once = 0
    dropping = 0

    @staticmethod
    def add_rescue():
        """
        if Rescue.once == 0 :
            Rescue.once = 1
            for x in range(0,Landscape.LANDSCAPE_MAX,50):
                game.runtime.rescue.append(Rescue(x * Landscape.SCALE))
        """
        if Rescue.dropping == 0:
            x = random.randint(0, Landscape.LANDSCAPE_MAX - 10)
            if random.randint(0, 1) == 0:
                x = (game.runtime.player.x_real + 200) % Landscape.LANDSCAPE_MAX
            game.runtime.rescue.append(Rescue(x * Landscape.SCALE))

        Rescue.dropping = 0

    def __init__(self, start_x):
        if Rescue.png is None:
            Rescue.png = Image.open(game.RESOURCES + "rescue.png")
            Rescue.img = ImageTk.PhotoImage(Rescue.png)
        self.x_to_landscape = start_x
        self.y_real = 700  # random.randint(200, game.SCREEN_Y)
        self.alien_target = None
        self.alien_target_countdown_to_free = 0
        self.amIFalling = True
        self.alienHasMe = False
        self.dead = False
        if self.x_to_landscape >= Landscape.LANDSCAPE_MAX * Landscape.SCALE - 1:
            self.x_to_landscape = self.x_to_landscape % (Landscape.LANDSCAPE_MAX * Landscape.SCALE - 1)

    def collision(self, x, y):
        x1 = self.x_to_landscape - Rescue.WIDTH / 2
        x2 = self.x_to_landscape + Rescue.WIDTH / 2
        y1 = self.y_real - Rescue.HEIGHT / 2
        y2 = self.y_real + Rescue.HEIGHT / 2

        # print(x1, y1, x2, y2, x, y)
        return game.Runtime.point_inside_rectangle(x1, y1, x2, y2, x, y)

    def i_am_an_alien_target_now(self, alien):
        self.alien_target_countdown_to_free = -500
        self.alien_target = alien

    def remove_rescue(self):
        self.dead = True

    def render(self, delta):

        if self.alien_target is not None:
            self.alien_target_countdown_to_free = self.alien_target_countdown_to_free + 1 * delta
            if self.alien_target.dead or self.alien_target_countdown_to_free >= 0:
                self.alien_target = None

        if not self.alienHasMe:
            if self.amIFalling \
                    and game.runtime.landscape.get_height(
                self.x_to_landscape / Landscape.SCALE) < self.y_real - Rescue.HEIGHT / 2 \
                    and self.y_real > Rescue.HEIGHT:
                self.y_real = self.y_real - 1 * delta
                Rescue.dropping = Rescue.dropping + 1 * delta
            else:
                self.amIFalling = False

        display, screen_x, screen_y = Landscape.map_to_screen(self.x_to_landscape, self.y_real)
        if display:
            game.runtime.main_canvas.create_image(screen_x, screen_y, image=Rescue.img)

        return display
