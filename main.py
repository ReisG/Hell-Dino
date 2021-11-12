from random import randint, choice

from Hell_dino.dino import Dino
from Hell_dino.enemies import Kaktus, Pterodactyl
from Hell_dino.interface.health_bar import Health
# from modules.interface.score import start

import arcade
import os

os.system('clear||cls')

WIDTH = 600
HEIGHT = 337

WIN_X = 55
WIN_Y = 30

SPEED = 5.5
GRAVITATION = 1
HORIZON = 80
ENEMY_SPAWN_DIST = 60



class Game(arcade.Window):
    def __init__(self, width: int = 800, height: int = 600,
                 title: str = 'Dino run', fullscreen: bool = False,
                 resizable: bool = False):
        super().__init__(width=width, height=height, title=title,
                         fullscreen=fullscreen, resizable=resizable)

        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (WIN_X, WIN_Y)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def setup(self):
        self.Dino = Dino(gravity=GRAVITATION)
        self.enemies = [Kaktus(x=self.width, y=HORIZON, speed=SPEED)]
        self.espd = ENEMY_SPAWN_DIST
        self.health = Health()

        self.score = 0
        self.speed = SPEED
        self.immortal = 0

        self.pause_screen = True

    def on_draw(self):
        arcade.start_render()
        arcade.draw_xywh_rectangle_outline(0, 0, self.width,
                                           HORIZON + 10, arcade.color.GRAY)
        for en in self.enemies:
            en.sprite.draw()

        self.Dino.draw()
        self.show_interface()

    def show_interface(self):
        if self.pause_screen:
            arcade.set_background_color(arcade.color.DARK_GRAY)
            if self.score == 0:
                arcade.draw_text(f"press \"ENTER\" to start", 220, self.height // 2, color=arcade.color.SMOKY_BLACK,
                                 font_size=15)
            else:
                arcade.draw_text(f"You died. Your score is {self.score // 10}", 180, (self.height // 2) + 20,
                                 color=arcade.color.SMOKY_BLACK,
                                 font_size=15)
                arcade.draw_text(f"press \"ENTER\" to start", 220, self.height // 2, color=arcade.color.SMOKY_BLACK,
                                 font_size=15)
        else:
            arcade.set_background_color(arcade.color.GHOST_WHITE)
            arcade.draw_text(f"score: {self.score // 10}", 0, self.height - 25, color=arcade.color.SMOKY_BLACK,
                             font_size=15)
            self.health.draw()

    def update(self, delta_time: float):
        self.immortal -= 1
        if self.pause_screen:
            return

        if self.immortal < 0:
            self.Dino.stop_blink()

        if self.enemies[-1].get_position() <= 200:
            self.spawn_enemy()
        if self.score % 250 == 0:
            self.speed_up()

        en = 0
        while en < len(self.enemies):
            col = arcade.check_for_collision_with_list(self.Dino.sprite, self.enemies[en].sprite_list)
            if len(col) != 0 and self.immortal < 0:
                self.health.health_down()
                self.immortal = 100
                self.Dino.start_blink()
            if self.enemies[en].terminate:
                self.enemies.pop(en)
            else:
                self.enemies[en].update(score=self.score)

            en += 1

        if self.health.is_dead():
            self.pause_screen = True
            return

        self.Dino.update()
        self.score += 1

    def spawn_enemy(self):
        self.enemies.append(choice([Kaktus(x=self.width, y=HORIZON, speed=self.speed), Pterodactyl(
            x=self.width, y=HORIZON, speed=(self.speed + randint(1, 3)))]))

    def speed_up(self):
        self.speed += 0.5
        self.espd -= 0.5 if self.espd > 0.5 else 0
        for en in self.enemies:
            en.speed += 0.5

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.Dino.jumping = True
        elif key == arcade.key.DOWN or key == arcade.key.D:
            self.Dino.squating = True

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.Dino.jumping = False
        elif key == arcade.key.DOWN or key == arcade.key.D:
            self.Dino.squating = False
        elif self.pause_screen and key == arcade.key.ENTER:
            self.setup()
            self.pause_screen = False


def main():
    game = Game(width=WIDTH, height=HEIGHT)
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
