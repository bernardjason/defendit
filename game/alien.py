from PIL import Image, ImageTk

import game
from game.explosion import Explosion
from game.landscape import Landscape
import random

from game.rescue import Rescue


class Alien:
    WIDTH = 32
    HEIGHT = 32
    SPEED = 1
    START_AGAIN = 500
    ASSENT = 0.5
    png = None
    img = None

    def __init__(self, start_x):
        if Rescue.png is None:
            Alien.png = Image.open(game.RESOURCES + "baddy.png")
            Alien.img = ImageTk.PhotoImage(Alien.png)
        self.x_to_landscape = start_x
        self.y_real = random.randint(200, game.SCREEN_Y)
        self.check_for_nearest_rescue_to_grab = 0
        self.once_aquired_wait_for = Alien.START_AGAIN
        self.x_target = None
        self.y_target = None
        self.fire = 300
        self.rescued:Rescue = None
        self.dead = False

    def old_collision(self, x, y):
        diff_x = abs(self.x_to_landscape - x)
        diff_y = abs(self.y_real - y)
        if diff_x < 10 and diff_y < 10:
            return True
        return False

    def collision(self, x, y):
        x1 = self.x_to_landscape - Alien.WIDTH / 2
        x2 = self.x_to_landscape + Alien.WIDTH / 2
        y1 = self.y_real - Alien.HEIGHT / 2
        y2 = self.y_real + Alien.HEIGHT / 2

        return game.Runtime.point_inside_rectangle(x1, y1, x2, y2, x, y)

    def got_rescued(self, rescued: Rescue):
        rescued.alienHasMe = True
        rescued.x_to_landscape = self.x_to_landscape
        self.rescued = rescued

    def handle_remove(self):
        Explosion.create(self.x_to_landscape,self.y_real)
        self.dead = True
        if self.rescued is not None:
            self.rescued.alienHasMe = False
            self.rescued.amIFalling = True

    def render(self,delta):
        self.check_for_nearest_rescue_to_grab = self.check_for_nearest_rescue_to_grab - 1*delta
        self.fire = self.fire - 1*delta

        if self.rescued is None:
            self.search_for_rescue_and_fire(delta)
        else:
            self.y_real = self.y_real + Alien.ASSENT
            self.rescued.y_real = self.y_real - Alien.HEIGHT
            if self.y_real >= game.SCREEN_Y:
                game.runtime.remove_alien_and_rescue(self,self.rescued)
                Explosion.create(self.x_to_landscape,self.y_real)

        display, screen_x, screen_y = Landscape.map_to_screen(self.x_to_landscape, self.y_real)
        if display:
            game.runtime.main_canvas.create_image(screen_x, screen_y, image=Alien.img)

        return display

    def search_for_rescue_and_fire(self,delta):
        if self.check_for_nearest_rescue_to_grab <= 0 and self.x_target is None:
            if  random.randint(0,1) == 0 :
                self.x_target, self.y_target = game.runtime.nearest_rescue(self.x_to_landscape, self.y_real, self)
            else:
                self.x_target, self.y_target = game.runtime.player.x_real * Landscape.SCALE,game.runtime.player.y_real

            self.check_for_nearest_rescue_to_grab = 200
            if self.x_target is not None:
                self.y_target = self.y_target + Alien.HEIGHT
        if self.fire <= 0:
            game.runtime.add_alien_phaser(self.x_to_landscape, self.y_real)
            self.fire = 180
        if self.x_target is not None:
            self.once_aquired_wait_for = self.once_aquired_wait_for - 1*delta
            if self.x_target < self.x_to_landscape:
                self.x_to_landscape = self.x_to_landscape - Alien.SPEED
            if self.x_target > self.x_to_landscape:
                self.x_to_landscape = self.x_to_landscape + Alien.SPEED
            if self.y_target < self.y_real:
                self.y_real = self.y_real - 1*delta
            if self.y_target > self.y_real:
                self.y_real = self.y_real + 1*delta
            if self.once_aquired_wait_for <= 0:
                self.once_aquired_wait_for = Alien.START_AGAIN
                self.x_target = None
                self.y_target = None
