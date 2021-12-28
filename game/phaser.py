import game
from game.landscape import Landscape


class Phaser:
    SIZE = 20
    ALIEN_SIZE = 5
    ALIEN = 0
    PLAYER = 1
    STEPS = 100
    ALIEN_SPEED = 3
    PLAYER_SPEED = 20

    def __init__(self, iam, start_x, start_y, direction_x, direction_y=0):
        self.iam = iam
        self.x_to_landscape = start_x * Landscape.SCALE  # + direction_x * 3
        self.y_real = start_y

        if self.iam == Phaser.PLAYER:
            self.timer = 120
            self.speed = Phaser.PLAYER_SPEED
        else:
            self.timer = 180
            self.speed = Phaser.ALIEN_SPEED

        self.direction_x, self.direction_y = game.nor(Landscape.SCALE * direction_x, direction_y)

    def render(self, delta):
        display, screen_x, screen_y = Landscape.map_to_screen(self.x_to_landscape, self.y_real)
        if display and self.iam is Phaser.PLAYER:
            game.runtime.main_canvas.create_rectangle(screen_x, screen_y, screen_x + self.direction_x * Phaser.SIZE,
                                                      screen_y + 2, fill="red")
        if display and self.iam is Phaser.ALIEN:
            game.runtime.main_canvas.create_rectangle(screen_x, screen_y, screen_x + Phaser.ALIEN_SIZE,
                                                      screen_y + Phaser.ALIEN_SIZE, fill="cyan")

        self.x_to_landscape = self.x_to_landscape + self.direction_x * self.speed * delta
        self.y_real = self.y_real + self.direction_y * self.speed * delta

        self.timer = self.timer - 1 * delta
        if self.timer > 0:
            remove = False
        else:
            remove = True

        return remove
