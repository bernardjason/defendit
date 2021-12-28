import collections
import math
from time import time
from tkinter import *
from tkinter.font import Font

import game
from game.alien import Alien
from game.explosion import Explosion
from game.landscape import Landscape
from game.phaser import Phaser
from game.playerShip import PlayerShip
from game.rescue import Rescue
from game.stars import Stars


class Runtime:
    fps_counter = 1
    fps = 1
    START_SCREEN = 0
    GAME_SCREEN = 1
    END_SCREEN = 2
    start_screen_draw_please = True
    end_screen_draw_please = True

    keyboard = {"Left": False, "Right": False, "space": False, "Shift_L": False, "Up": False, "Down": False,
                "Escape": False}

    def __init__(self):
        self.tk = Tk()
        self.text_header_canvas = Canvas(self.tk, bg="green")
        self.text_header_canvas.pack(fill=X)
        self.topLabelText = StringVar()
        Label(self.text_header_canvas, textvariable=self.topLabelText, bg="green", fg="black").pack(side=LEFT)
        self.main_canvas = Canvas(self.tk, bg="black")
        self.main_canvas.pack(fill=BOTH, expand=True)
        self.click = 0
        self.tk.geometry(format(f"{game.SCREEN_X}x{game.SCREEN_Y}"))
        self.landscape = Landscape()
        self.player = PlayerShip()
        for char in ["Left", "Right", "Up", "Down", "space", "Shift_L", "Escape"]:
            self.tk.bind(f"<KeyPress-{char}>", Runtime.key_pressed)
            self.tk.bind(f"<KeyRelease-{char}>", Runtime.key_released)
        self.timeStarted = self.unix_time_millis()

        self.aliens: list[Alien] = []
        self.phasers: list[Phaser] = []
        self.rescue: list[Rescue] = []
        self.delta = game.BEST_REFRESH_RATE / game.REFRESH_RATE * game.SPEED_UP
        self.delta
        self.reduce_frame_rate = 0
        self.screen = {
            Runtime.START_SCREEN: lambda: self.start_screen_render(),
            Runtime.GAME_SCREEN: lambda: self.main_game_render(),
            Runtime.END_SCREEN: lambda: self.end_screen_render()
        }
        self.current_screen = Runtime.START_SCREEN

        Stars.create()

    def reset_game(self):
        self.player.reset_player()
        self.aliens.clear()
        self.rescue.clear()
        Explosion.particles.clear()

    def add_phaser(self, start_x, start_y, direction_x):
        self.phasers.append(Phaser(Phaser.PLAYER, start_x, start_y, direction_x, 0))

    def add_alien_phaser(self, start_x, start_y):
        direction_x = self.player.x_real - start_x / Landscape.SCALE

        dist = math.hypot(self.player.x_real - start_x / Landscape.SCALE, start_y - self.player.y_real - start_y)
        if direction_x != 0:
            direction_y = self.player.y_real - start_y
        else:
            direction_y = 1

        if dist < 1000:
            self.phasers.append(Phaser(Phaser.ALIEN, start_x / Landscape.SCALE, start_y, direction_x, direction_y))

    def nearest_rescue(self, x, y, alien):
        distance = {}

        for r in self.rescue:
            if r.alien_target is None:
                dist = math.hypot(r.x_to_landscape - x, r.y_real - y)
                distance[dist] = r

        od = collections.OrderedDict(sorted(distance.items()))
        if len(od) > 0:
            rescue_me: Rescue = list(od.values())[0]
            rescue_me.alien_target = alien
            return rescue_me.x_to_landscape, self.landscape.get_height(rescue_me.x_to_landscape / Landscape.SCALE)
        else:
            return None, None

    level_aliens = [1800, 1200, 800, 700, 600, 500, 400, 300]

    def add_aliens(self):
        if len(self.aliens) != 0:
            return

        for x in range(400, Landscape.LANDSCAPE_MAX * Landscape.SCALE,
                       Runtime.level_aliens[self.player.level % len(Runtime.level_aliens)]):
            self.aliens.append(Alien(x))

    @staticmethod
    def key_pressed(event):
        Runtime.keyboard[event.keysym] = True

    @staticmethod
    def key_released(event):
        Runtime.keyboard[event.keysym] = False

    def mainloop(self):
        self.tk.after(10, self.render)
        self.tk.mainloop()

    @staticmethod
    def unix_time_millis():
        return int(time() * 1000)

    @staticmethod
    def point_inside_rectangle(x1, y1, x2, y2, px, py):
        return px >= x1 and px <= x2 and py >= y1 and py <= y2

    def remove_alien_and_rescue(self, alien, rescued=None):
        if rescued is not None:
            rescued.remove_rescue()
            if rescued in self.rescue:
                self.rescue.remove(rescued)
        if alien is not None:
            alien.handle_remove()
            if alien in self.aliens:
                self.aliens.remove(alien)

    def render(self):
        self.screen[self.current_screen]()

    title = {"red": "B",
             "yellow": "e",
             "green": "r",
             "snow": "n",
             "pink": "i",
             "cyan": "e",
             "magenta": "s",
             "gold": "o",
             "orange": "f",
             "blue": "t"
             }

    def start_screen_render(self):
        self.click = self.click + 1
        if Runtime.start_screen_draw_please:
            Runtime.start_screen_draw_please = False
            self.main_canvas.delete("all")
            self.draw_bernie_soft()

            instructions = """
            Avoid the landscape, kill the aliens and try and rescue the survivors.
            Arrow keys to change direction and up/down
            shift left for thrust
            space fire
            
            Press space to start or escape to exit
            """
            self.main_canvas.create_text(400, game.SCREEN_Y / 2, text=instructions, fill="cyan")

        if Runtime.keyboard["space"]:
            self.start_the_game()
        if Runtime.keyboard["Escape"]:
            sys.exit(0)
        self.tk.after(20, self.render)

    def end_screen_render(self):
        self.click = self.click + 1
        if Runtime.end_screen_draw_please:
            Runtime.end_screen_draw_please = False
            self.draw_bernie_soft()

            instructions = f"""
            Final score {self.player.score} reached level {self.player.level}
            Press space to start or escape to exit
            """
            self.main_canvas.create_text(400, game.SCREEN_Y / 2, text=instructions, fill="cyan")

        if Runtime.keyboard["space"]:
            self.start_the_game()
        if Runtime.keyboard["Escape"]:
            sys.exit(0)
        self.tk.after(20, self.render)

    def draw_bernie_soft(self):
        x = 90
        for k, v in Runtime.title.items():
            self.main_canvas.create_text(x, 100, text=v, fill=k, font=Font(size=120, slant='italic'))
            x = x + 90
        gap = 4
        for x in range(0, game.SCREEN_X, gap):
            for y in range(10, int(game.SCREEN_Y / 2), gap):
                self.main_canvas.create_rectangle(x, y, x + 2, y + 2, fill="black")

    def start_the_game(self):
        Runtime.keyboard["space"] = False
        self.timeStarted = self.unix_time_millis()
        self.reset_game()
        self.current_screen = Runtime.GAME_SCREEN

    def dont_fire_at_player_for_a_while(self):
        for a in self.aliens:
            a.fire = 300
        self.phasers.clear()

    def phasers_remove(self, p):
        if p in self.phasers:
            self.phasers.remove(p)

    def main_game_render(self):
        start_time = self.unix_time_millis()
        self.add_aliens()
        self.click = self.click + 1

        Rescue.add_rescue()
        self.main_canvas.delete("all")
        Stars.render()
        self.landscape.render()
        self.player.render(self.delta)

        for r in self.rescue:
            r.render(self.delta)
            if r.collision((self.player.x_real - PlayerShip.BACK) * Landscape.SCALE, self.player.y_real) or \
                    r.collision((self.player.x_real + PlayerShip.FRONT) * Landscape.SCALE, self.player.y_real) or \
                    r.collision(self.player.x_real * Landscape.SCALE, self.player.y_real - PlayerShip.HEIGHT / 2) or \
                    r.collision(self.player.x_real * Landscape.SCALE, self.player.y_real):
                self.remove_alien_and_rescue(alien=None, rescued=r)
                self.player.rescued(r.alienHasMe)
            if not r.alienHasMe:
                for a in self.aliens:
                    if r.collision(a.x_to_landscape, a.y_real - Alien.HEIGHT / 2):
                        a.got_rescued(r)
            for p in self.phasers:
                if p.iam == Phaser.PLAYER and (
                        r.collision(p.x_to_landscape - Phaser.PLAYER_SPEED / 2, p.y_real) or
                        r.collision(p.x_to_landscape, p.y_real)) \
                        :
                    self.remove_alien_and_rescue(alien=None, rescued=r)
                    self.phasers_remove(p)

        for a in self.aliens:
            a.render(self.delta)
            if a.collision((self.player.x_real - PlayerShip.BACK) * Landscape.SCALE, self.player.y_real) or \
                    a.collision((self.player.x_real + PlayerShip.FRONT) * Landscape.SCALE, self.player.y_real) or \
                    a.collision(self.player.x_real * Landscape.SCALE, self.player.y_real):
                self.player.been_hit()
                self.dont_fire_at_player_for_a_while()
                self.remove_alien_and_rescue(a)

            for p in self.phasers:
                if p.iam == Phaser.PLAYER and (
                        a.collision(p.x_to_landscape - Phaser.PLAYER_SPEED / 2, p.y_real) or
                        a.collision(p.x_to_landscape, p.y_real)):
                    self.player.hit_alien()
                    self.remove_alien_and_rescue(a)
                    self.phasers_remove(p)

        for p in self.phasers:
            remove = p.render(self.delta)
            if p.iam is Phaser.ALIEN and self.point_inside_rectangle(
                    (self.player.x_real - PlayerShip.BACK) * Landscape.SCALE, self.player.y_real - 8,
                    (self.player.x_real + PlayerShip.FRONT) * Landscape.SCALE, self.player.y_real + 8,
                    p.x_to_landscape, p.y_real
            ):
                self.player.been_hit()
                self.dont_fire_at_player_for_a_while()
                self.phasers_remove(p)

            if remove:
                if p in self.phasers:
                    self.phasers_remove(p)

        Explosion.render(self.delta)

        self.fps_counter = self.fps_counter + 1
        since = (start_time - self.timeStarted) / 1000
        self.fps = round(self.fps_counter / since)
        show = f"FPS={int(self.fps)} rescued={self.player.rescue_count} hits={self.player.hits} lives={self.player.lives} score={self.player.score} level={self.player.level}"
        self.topLabelText.set(show)

        elapsed_time = self.unix_time_millis() - start_time
        sleep = int(1000 / game.REFRESH_RATE - elapsed_time)
        if sleep < 0:
            self.delta = 1 / abs(sleep) + game.BEST_REFRESH_RATE / game.REFRESH_RATE * game.SPEED_UP
            sleep = 0
            print(f".. {elapsed_time}")
            self.reduce_frame_rate = self.reduce_frame_rate - 1
            if self.reduce_frame_rate <= 0:
                game.REFRESH_RATE = game.REFRESH_RATE - 1
                self.reduce_frame_rate = 30
                print("REDUCE FRAME RATE ", game.REFRESH_RATE)
        else:
            self.delta = game.BEST_REFRESH_RATE / game.REFRESH_RATE * game.SPEED_UP

        if len(self.aliens) == 0:
            self.player.level = self.player.level + 1
            self.player.lives = self.player.lives + 1
        if self.player.lives == 0:
            self.current_screen = Runtime.END_SCREEN
            Runtime.end_screen_draw_please = True

        if Runtime.keyboard["Escape"]:
            sys.exit(0)
        self.tk.after(sleep, self.render)
