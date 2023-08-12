from math import ceil

from pygame import Surface

import helpers
import settings
from health_bar import HealthBar


class Monster:

    def __init__(self,
                 image: Surface,
                 x_pos: float,
                 y_pos: float,
                 health: int):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.gold_reward = 0

        self.max_health = 0
        self.health = health

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x_pos, self.y_pos

        self.health_bar_width = 200
        self.health_bar = HealthBar(x=self.x_pos - 20,
                                    y=self.rect.bottomleft[1] + 15,
                                    width=self.health_bar_width,
                                    height=40,
                                    color=(255, 20, 15)
                                    )
        self.health_bar_pad = HealthBar(x=self.x_pos - 20,
                                        y=self.rect.bottomleft[1] + 15,
                                        width=self.health_bar_width,
                                        height=40,
                                        color=(128, 128, 128)
                                        )

    @property
    def monster_pos(self):
        return self.x_pos, self.y_pos

    @property
    def is_dead(self):
        return self.health <= 0

    @property
    def get_new_max_health(self):
        return ceil(settings.last_monster_health * settings.monster_health_scale_value)

    @property
    def get_new_gold_reward(self):
        return ceil(settings.last_monster_gold_reward * settings.monster_initial_gold_reward_scale)

    def create_health_surface(self) -> Surface:
        formatted_health = helpers.numbers_format(self.health)
        formatted_max_health = helpers.numbers_format(self.max_health)
        return helpers.create_font(f"{formatted_health}/{formatted_max_health}",
                                   "Georgia",
                                   30,
                                   (0, 0, 0)
                                   ).convert_alpha()

    def prepare_text_for_display(self) -> tuple:
        surface = self.create_health_surface()
        center_x = helpers.calculate_center(self.health_bar_width, surface.get_width()) + self.health_bar.rect.x
        center_y = helpers.calculate_center(self.health_bar.rect.height, surface.get_height()) + self.health_bar.rect.y

        return surface, (center_x, center_y)

    def set_max_health(self, max_health: float):
        self.max_health = max_health

    def take_damage(self, amount: float):
        self.health_bar.lower_bar_width(current_health=self.health,
                                        max_health=self.max_health,
                                        remove_health=amount)

        self.health -= amount

    def prepare_for_next_spawn_after_death(self, stage_cleared=True):
        if stage_cleared:
            new_health = self.get_new_max_health
            new_gold = self.get_new_gold_reward

            settings.last_monster_health = new_health
            settings.last_monster_gold_reward = new_gold

            self.set_max_health(new_health)
            self.gold_reward = settings.last_monster_gold_reward

        self.health = self.max_health
        self.health_bar.rect.width = self.health_bar_width

    def give_reward(self):
        return self.gold_reward
