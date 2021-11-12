from os import system
import arcade


class Dino:
    JUMP = 13

    def __init__(self, x=75, y=0, gravity=0, hor=100):
        self.GRAVITATION = gravity
        self.HORIZON = hor

        self.tick = 0

        self.color = arcade.color.DARK_BLUE_GRAY  # (12, 12, 12, 1)

        self.vert_speed = 0

        self.squating = False
        self.jumping = False

        self.sprite_list = arcade.SpriteList()
        img = "img/dino_01.png"
        self.sprite = arcade.Sprite(img, 0.5)
        self.sprite.center_x = 50
        self.sprite.center_y = 100
        self.sprite_list.append(self.sprite)

        self.blink = True

    def update(self):
        self.jump()
        self.squat()
        self.tick += 1
        self.sprite_list.update()

    def draw(self):
        if self.blink:
            if self.tick % 10 > 5:
                alpha = 155
            else:
                alpha = 235
        else:
            alpha = 255
        self.sprite.alpha = alpha
        self.sprite_list.draw()

    def jump(self):
        if self.sprite.center_y == self.HORIZON and self.jumping:
            self.vert_speed = self.JUMP
        elif self.sprite.center_y <= self.HORIZON and self.vert_speed <= 0:
            self.vert_speed = 0
            self.sprite.center_y = self.HORIZON
        else:
            self.vert_speed -= self.GRAVITATION

        self.sprite.change_y = self.vert_speed

    def squat(self):
        if self.squating:
            self.sprite.scale = 0.4
            self.HORIZON = 90
            self.vert_speed -= self.GRAVITATION * 1.5
        else:
            self.sprite.scale = 0.5
            self.HORIZON = 100

    def get_position(self):
        return self.sprite_list[0].center_x
    
    def start_blink(self):
        self.blink = True

    def stop_blink(self):
        self.blink = False