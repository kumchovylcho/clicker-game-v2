from typing import Sequence


class CoinRotater:

    def __init__(self, coin_x: int, coin_y: int, images: Sequence):
        self.images = images
        self.index = 0
        self.loop_speed = 0.18
        self.coin_x = coin_x
        self.coin_y = coin_y

    @property
    def get_coin_pos(self):
        return self.coin_x, self.coin_y

    @property
    def get_current_image(self):
        return self.images[int(self.index)]

    def rotate_coin(self, screen):
        self.index += self.loop_speed

        if self.index >= len(self.images):
            self.index = 0

        screen.blit(self.get_current_image, self.get_coin_pos)