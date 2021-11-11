from random import randint, choice
from time import time

import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

POS_X = 55
POS_Y = 1

SPEED = 2
GRAVITATION = 0.6
HORIZONT = 80
ENEMY_KD = 50


class Dino():
    def __init__(self):
        self.width = 45
        self.height = 55
        self.pos_x = 75
        self.pos_y = HORIZONT

        self.color = arcade.color.DARK_BLUE_GRAY  # (12, 12, 12, 1)

        self.speed_v = 0

        self.hold = False
        self.jumping = False
        self.img = arcade.load_texture("img/dino_01.png")

    def draw(self):
        # arcade.draw_xywh_rectangle_filled(self.pos_x, self.pos_y, self.width, self.height, self.color)
        arcade.draw_lrwh_rectangle_textured(
            self.pos_x, self.pos_y, self.width, self.height, self.img)

    def update(self):
        if self.jumping:
            self.jump()
        if self.pos_y > HORIZONT:
            self.pos_y += self.speed_v
            self.speed_v -= GRAVITATION
        else:
            self.pos_y = 80
            self.speed_v = 0

        if self.hold:
            self.height = 30
            self.width = 20
        else:
            self.height = 55
            self.width = 45

    def jump(self):
        if self.pos_y == HORIZONT:
            self.speed_v = 9.5
            self.pos_y += self.speed_v


class Kaktus:
    def __init__(self):
        self.speed = SPEED

        self.color = arcade.color.BLUE_BELL
        self.pos_x = SCREEN_WIDTH + 25
        self.pos_y = HORIZONT
        self.width = 25
        w = randint(0, 100)
        if w <= 60:
            self.width = 25
            self.img = arcade.load_texture("img/kaktus_01.png")
        elif w <= 85:
            self.width = 40
            self.img = arcade.load_texture("img/kaktus_03.png")
        else:
            self.width = 70
            self.img = arcade.load_texture("img/kaktus_02.png")
        self.height = 60

        self.terminate = False

    def draw(self, frame):
        # arcade.draw_xywh_rectangle_filled(self.pos_x, self.pos_y, self.width, self.height, self.color)
        arcade.draw_lrwh_rectangle_textured(
            self.pos_x, self.pos_y, self.width, self.height, self.img)

    def update(self):
        # self.sprite.update()
        if not self.terminate:
            self.pos_x -= self.speed
        if self.pos_x < (-30):
            self.terminate = True


class Pter:
    height = [0, 35, 80]

    def __init__(self):
        self.speed = SPEED

        self.color = arcade.color.BLUE_BELL
        self.pos_x = SCREEN_WIDTH + 25
        self.pos_y = HORIZONT + choice(Pter.height)
        self.width = 50
        self.height = 35

        self.terminate = False

        self.setup()
        self.img = [arcade.load_texture(
            f"img/pter_0{i+1}.png") for i in range(2)]

    def draw(self, score):
        # arcade.draw_xywh_rectangle_filled(self.pos_x, self.pos_y, self.width, self.height, self.color)
        frame = score // 10 % len(self.img)
        arcade.draw_lrwh_rectangle_textured(
            self.pos_x, self.pos_y, self.width, self.height, self.img[frame])

    def update(self):
        if not self.terminate:
            self.pos_x -= self.speed
        if self.pos_x < (-30):
            self.terminate = True

    def setup(self):
        pass


class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height, "Bromine Dino")
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{POS_X},{POS_Y}"
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def setup(self):
        # Настроить игру здесь
        self.dino = Dino()
        self.enemy_list = []
        self.enemy_list.append(Kaktus())
        self.enemy_kd = ENEMY_KD
        self.score = 0
        self.pause_screen = True

        self.counter = 0
        self.counter_time = time()

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        arcade.draw_xywh_rectangle_outline(
            0, 0, SCREEN_WIDTH, HORIZONT + 10, arcade.color.GRAY)
        # self.dino.draw()
        for en in self.enemy_list:
            en.draw(self.score)
        self.dino.draw()
        if self.pause_screen:
            if self.score == 0:
                arcade.draw_text(f"press \"ENTER\" to start", 220, SCREEN_HEIGHT // 2, color=arcade.color.SMOKY_BLACK,
                                 font_size=15, font_name="img/joystix_monospace.ttf")
            else:
                arcade.draw_text(f"You died. Your score is {self.score // 10}", 180, (SCREEN_HEIGHT // 2) + 20,
                                 color=arcade.color.SMOKY_BLACK,
                                 font_size=15, font_name="img/joystix_monospace.ttf")
                arcade.draw_text(f"press \"ENTER\" to start", 220, SCREEN_HEIGHT // 2, color=arcade.color.SMOKY_BLACK,
                                 font_size=15, font_name="img/joystix_monospace.ttf")
        else:
            arcade.draw_text(f"score: {self.score // 10}", 0, SCREEN_HEIGHT - 25, color=arcade.color.SMOKY_BLACK,
                             font_size=15, font_name="img/joystix_monospace.ttf")
        self.counter += 1
        FPS = self.counter / (time() - self.counter_time + 0.01)
        # arcade.draw_text(f"{FPS:3}", 0, SCREEN_HEIGHT - 45, color=arcade.color.COOL_BLACK,
        #                  font_size=20)

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        if self.pause_screen:
            return

        global ENEMY_KD

        self.score += 1
        self.enemy_kd -= 1

        if self.enemy_kd < 0:
            self.spawn_enemy()
            self.enemy_kd = ENEMY_KD

        if self.score % 1000 == 0:
            for en in self.enemy_list:
                en.speed += 2

            global SPEED
            SPEED += 2
            ENEMY_KD -= 3

        l = len(self.enemy_list) - 1
        for en in range(l):
            if self.enemy_list[en].terminate:
                self.enemy_list.pop(0)
                l -= 1
            else:
                self.enemy_list[en].update()

            if check_collision(self.dino, self.enemy_list[en]):
                self.pause_screen = True
                return

        self.dino.update()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.dino.jumping = True
        elif key == arcade.key.DOWN or key == arcade.key.D:
            self.dino.hold = True

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.dino.jumping = False
        elif key == arcade.key.DOWN or key == arcade.key.D:
            self.dino.hold = False
        elif self.pause_screen and key == arcade.key.ENTER:
            global SPEED
            global ENEMY_KD
            ENEMY_KD = 60
            SPEED = 8
            self.pause_screen = False
            self.score = 0
            self.dino.pos_y = HORIZONT
            self.enemy_list = [Kaktus()]

    def spawn_enemy(self):
        en = randint(0, 1000)
        if en <= 600:
            self.enemy_list.append(Kaktus())
        else:
            self.enemy_list.append(Pter())


def check_collision(obj1, obj2):
    rect1 = [[obj1.pos_x, obj1.pos_y], [
        obj1.pos_x + obj1.width, obj1.pos_y + obj1.height]]
    rect2 = [[obj2.pos_x, obj2.pos_y], [
        obj2.pos_x + obj2.width, obj2.pos_y + obj2.height]]

    if rect1[0][0] <= rect2[0][0] <= rect1[1][0] and rect1[0][1] <= rect2[0][1] <= rect1[1][1]:
        return True
    if rect1[0][0] <= rect2[1][0] <= rect1[1][0] and rect1[0][1] <= rect2[1][1] <= rect1[1][1]:
        return True
    return False


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


main()
