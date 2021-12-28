from PIL import Image, ImageTk

import game.landscape
import game.runtime


class PlayerShip:
    BACK = 6
    FRONT = 6
    HEIGHT = 10
    FROM_SIDE = 150
    DIRECTION = 5
    UPDOWN = 2
    INERTIA = 20
    CHANGE_SCREEN_POSITION_SIDE_SPEED = 7
    SHIP_BOTTOM = 8

    def __init__(self):
        self.phaser_last_fired = 0
        self.x_real = 0
        self.y_real = game.SCREEN_Y - PlayerShip.HEIGHT
        self.screen_x = 0
        self.screen_y = 0
        self.direction = PlayerShip.DIRECTION
        png = Image.open(game.RESOURCES + "ship_right.png")
        self.img_right = ImageTk.PhotoImage(png)
        png = Image.open(game.RESOURCES + "ship_left.png")
        self.img_left = ImageTk.PhotoImage(png)
        self.player_from_side = PlayerShip.FROM_SIDE
        self.set_target_side = PlayerShip.FROM_SIDE
        self.rescue_count = 0
        self.hits = 0
        self.speed = 0
        self.level = 0
        self.score = 0
        self.lives = 0
        self.reset_player()

    def reset_player(self):
        self.phaser_last_fired = 0
        self.x_real = 0
        self.y_real = game.SCREEN_Y - PlayerShip.HEIGHT
        self.screen_x = 0
        self.screen_y = 0
        self.direction = PlayerShip.DIRECTION
        self.rescue_count = 0
        self.hits = 0
        self.speed = 0
        self.level = 1
        self.score = 0
        self.lives = 3

    def move_to_side(self):
        if self.direction > 0 and self.player_from_side <= self.set_target_side:
            self.player_from_side = self.set_target_side
            return
        if self.direction < 0 and self.player_from_side >= self.set_target_side:
            self.player_from_side = self.set_target_side
            return
        self.player_from_side = self.player_from_side - self.direction * PlayerShip.CHANGE_SCREEN_POSITION_SIDE_SPEED

    def been_hit(self, take_life=1):
        self.hits = self.hits + 1
        self.lives = self.lives - take_life
        game.explosion.Explosion.create(self.x_real * game.landscape.Landscape.SCALE, self.y_real)
        self.y_real = game.SCREEN_Y - PlayerShip.HEIGHT
        from game.sound import explosion
        explosion()
        self.speed = 0

    def hit_alien(self):
        self.score = self.score + 1
        from game.sound import hit_alien
        hit_alien()

    def rescued(self, alienhasMe):
        from game.sound import rescued
        if alienhasMe:
            self.score = self.score + 1000
        else:
            self.score = self.score + 100
        self.rescue_count = self.rescue_count + 1
        #game.runtime.add_phaser(self.x_real, self.y_real, self.direction)
        rescued()

    def render(self, delta):

        self.phaser_last_fired = self.phaser_last_fired + 1 * delta
        old_x = self.x_real
        old_y = self.y_real
        self.move_to_side()

        if game.runtime.keyboard["Up"]:
            self.y_real = self.y_real + PlayerShip.UPDOWN * delta
            if self.y_real > game.SCREEN_Y - PlayerShip.HEIGHT:
                self.y_real = game.SCREEN_Y - PlayerShip.HEIGHT
        if game.runtime.keyboard["Down"]:
            self.y_real = self.y_real - PlayerShip.UPDOWN * delta
        if game.runtime.keyboard["Shift_L"]:
            self.speed = self.speed + 1 / delta / PlayerShip.INERTIA
            if self.speed > 1:
                self.speed = 1
        else:
            self.speed = self.speed - 1 / delta / PlayerShip.INERTIA
            if self.speed < 0:
                self.speed = 0

        if game.runtime.keyboard["Left"]:
            self.direction = -PlayerShip.DIRECTION;
            # self.player_from_side = game.SCREEN_X - PlayerShip.FROM_SIDE
            self.set_target_side = game.SCREEN_X - PlayerShip.FROM_SIDE
        if game.runtime.keyboard["Right"]:
            self.direction = PlayerShip.DIRECTION;
            # self.player_from_side = PlayerShip.FROM_SIDE
            self.set_target_side = PlayerShip.FROM_SIDE
        if game.runtime.keyboard["space"] and self.phaser_last_fired > 0:
            self.phaser_last_fired = -25
            game.runtime.add_phaser(self.x_real, self.y_real, self.direction)
            from game.sound import phaser_fire
            phaser_fire()

        self.x_real = self.x_real + self.direction * self.speed * delta

        if self.x_real >= game.landscape.Landscape.LANDSCAPE_MAX:
            self.x_real = self.x_real - game.landscape.Landscape.LANDSCAPE_MAX
        if self.x_real < 0:
            self.x_real = self.x_real + game.landscape.Landscape.LANDSCAPE_MAX

        # print(game.runtime.landscape.get_height(self.x_real), self.y_real)

        ship_bottom = self.y_real - PlayerShip.SHIP_BOTTOM
        if game.runtime.landscape.get_height(self.x_real) > ship_bottom or \
                game.runtime.landscape.get_height(self.x_real - PlayerShip.BACK) > ship_bottom or \
                game.runtime.landscape.get_height(self.x_real + PlayerShip.FRONT) > ship_bottom or \
                game.runtime.landscape.get_height(self.x_real - PlayerShip.BACK) > self.y_real or \
                game.runtime.landscape.get_height(self.x_real + PlayerShip.FRONT) > self.y_real:
            self.x_real = old_x
            self.y_real = old_y
            self.been_hit(take_life=0)

        self.screen_y = game.SCREEN_Y - int(self.y_real)
        self.screen_x = self.player_from_side
        if self.direction == PlayerShip.DIRECTION:
            game.runtime.main_canvas.create_image(self.screen_x, self.screen_y, image=self.img_right)
        else:
            game.runtime.main_canvas.create_image(self.screen_x, self.screen_y, image=self.img_left)
