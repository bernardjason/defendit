import random
from math import *

import game
import game.playerShip


class Landscape:
    LANDSCAPE_MAX = 4000
    SCALE = 3

    def __init__(self):
        self.heights = []
        a = 0
        limit_height = 10
        for point in range(0, Landscape.LANDSCAPE_MAX):
            if point % 100 == 0:
                limit_height = random.randint(0, 10) * 4
            y = sin(radians(a)) * 100 - limit_height
            if y < 0:
                y = abs(y)

            add = random.randint(-10, 10)
            if add < 0:
                add = 0
            a = a + add
            if point < 200 or point > 300:
                self.heights.append(y * 3)
            else:
                self.heights.append(175)

        self.height_length = len(self.heights)

    def get_height(self, index):
        if index < 0:
            index = index + self.height_length

        if index >= self.height_length:
            index = index - self.height_length
        return self.heights[int(index / Landscape.SCALE)]

    def render(self):
        previous_x = 0
        previous_y = 0
        """
        nearest_height = int(player_position_x)  # - game.runtime.player.player_from_side )
        if game.runtime.player.direction == game.playerShip.PlayerShip.DIRECTION:
            nearest_height = nearest_height - game.runtime.player.player_from_side
        else:
            nearest_height = nearest_height -int(game.SCREEN_X/2) #game.runtime.player.player_from_side - 200
        """
        start_x = int(game.runtime.player.x_real)
        if game.runtime.player.direction == game.playerShip.PlayerShip.DIRECTION:
            start_x = start_x - game.runtime.player.player_from_side / Landscape.SCALE
        else:
            start_x = start_x - int(
                game.runtime.player.player_from_side / Landscape.SCALE)  # game.runtime.player.player_from_side - 200

        x = 0
        for bars in range(int(start_x), int(start_x + (game.SCREEN_X / Landscape.SCALE))):
            x = x + Landscape.SCALE
            y = self.get_height(bars)
            game.runtime.main_canvas.create_line(previous_x, game.SCREEN_Y - previous_y, x, game.SCREEN_Y - y,
                                                 fill="green")
            previous_y = y
            previous_x = x

    @staticmethod
    def map_to_screen(x_real, y_real):
        screen_x = x_real - game.runtime.player.x_real * Landscape.SCALE + game.runtime.player.player_from_side
        if screen_x >= Landscape.LANDSCAPE_MAX:
            screen_x = screen_x - Landscape.LANDSCAPE_MAX * Landscape.SCALE
        if screen_x < 0:
            screen_x = screen_x + Landscape.LANDSCAPE_MAX * Landscape.SCALE
        screen_y = game.SCREEN_Y - y_real
        if screen_x < -64 or screen_x > game.SCREEN_X + 64:
            return False, 0, 0
        return True, screen_x, screen_y
