import arcade


class Health:
    HEALTH = 3
    def __init__(self):
        self.health = 0
        self.hearts = []
        self.setup()

    def setup(self):
        self.health = 2 * self.HEALTH
        heart_files = ['img/heart_no.png', 'img/heart_half.png', 'img/heart_full.png']

        pos_x = 580
        pos_y = 320

        for i in range(self.HEALTH):
            heart = arcade.SpriteList()
            for sp in range(3):
                sprite = arcade.Sprite(heart_files[sp], 0.125)
                sprite.center_x = pos_x
                sprite.center_y = pos_y
                heart.append(sprite)
            self.hearts.append(heart)
            pos_x -= 40

    def draw(self):
        hp = self.health
        for i in range(self.HEALTH):
            if hp >= 2:
                lv = 2
            elif hp == 1:
                lv = 1
            else:
                lv = 0
            hp -= 2
            self.hearts[i][lv].draw()

    def update(self):
        pass

    def health_down(self, cost: float = 1):
        self.health -= cost

    def is_dead(self):
        if self.health == 0:
            return True
        return False
