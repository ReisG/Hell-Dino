from random import randint, choice
import arcade


class Enemy:
    def __init__(self, width=50, height=50, x=0, y=0,
                 speed=10):
        self.width = width
        self.height = height

        self.position = [x, y]
        self.speed = speed
        self.terminate = False

        self.sprite_list = arcade.SpriteList()

    def setup(self):
        pass

    def get_position(self):
        return self.sprite_list[0].center_x


class Kaktus(Enemy):
    WIDTH_VARIATIONS = [25, 70, 40]

    def __init__(self, width=50, height=50, x=0, y=0, speed=10):
        super().__init__(width=width, height=height, x=x, y=y, speed=speed)

        self.width = choice(self.WIDTH_VARIATIONS)

        img = f'img/kaktus_0{self.WIDTH_VARIATIONS.index(self.width) + 1}.png'
        self.sprite = arcade.Sprite(img, 0.5)
        self.sprite.center_x = 630
        self.sprite.center_y = 105
        self.sprite.change_x = -self.speed

        self.sprite_list.append(self.sprite)

    def update(self, score=None):
        self.sprite_list.update()

        if self.sprite_list[0].center_x <= -50:
            self.terminate = True


class Pterodactyl(Enemy):
    Y_HEIGHT = [100, 130, 180]

    def __init__(self, width=50, height=35, x=0, y=0, speed=10):
        super().__init__(width=width, height=height, x=x, y=y, speed=speed)

        self.setup()

    def setup(self):
        self.height = choice(self.Y_HEIGHT)

        for i in range(2):
            img = f'img/pter_0{i + 1}.png'
            self.sprite = arcade.Sprite(img, 0.5)
            self.sprite.center_x = 630
            self.sprite.center_y = self.height
            self.sprite.change_x = -self.speed
            self.sprite_list.append(self.sprite)

    def update(self, score = 2):
        self.sprite = self.sprite_list[(score // 11) % 2]
        self.sprite_list.update()

        if self.sprite_list[0].center_x <= -50:
            self.terminate = True
