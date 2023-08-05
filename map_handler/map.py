from pygame import Surface
from collections import deque

from map_handler.monster import Monster
from platform import Platform


class Map:

    def __init__(self, background_img: Surface, platform: Platform):
        self.background_img = background_img
        self.monsters = deque()
        self.platform = platform

    def add_monster(self, monster: Monster):
        self.monsters.appendleft(monster)

