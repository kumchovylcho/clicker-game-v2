from pygame import Surface


class Monster:

    def __init__(self, image: Surface, health: int):
        self.max_health = health
        self.health = health
        self.image = image

