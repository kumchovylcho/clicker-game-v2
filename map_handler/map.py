from pygame import Surface
from typing import Sequence

from map_handler.monster import Monster
from map_handler.platform import Platform


class Map:

    def __init__(self, background_img: Surface, platform: Platform):
        self.background_img = background_img
        self.monsters = []
        self.platform = platform
        self.current_monster_index = 0

    @property
    def is_last_monster(self):
        return self.current_monster_index == len(self.monsters) - 1

    def add_monsters(self, monsters: Sequence[Monster]):
        for monster in monsters:
            self.monsters.append(monster)

    def spawn_next_monster(self):
        self.current_monster_index += 1

    def reset_monster_index(self):
        self.current_monster_index = 0

