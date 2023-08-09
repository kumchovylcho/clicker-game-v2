from pygame import Surface

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
        return round(self.max_health * settings.monster_health_scale_value)

    def set_max_health(self, max_health: float):
        self.max_health = max_health

    def take_damage(self, amount: float):
        self.health_bar.lower_bar_width(current_health=self.health,
                                        max_health=self.max_health,
                                        remove_health=amount)

        self.health -= amount
        if self.is_dead:
            self.prepare_for_next_spawn_after_death()

    def prepare_for_next_spawn_after_death(self):
        self.set_max_health(self.get_new_max_health)
        self.health = self.max_health
        self.health_bar.width = self.health_bar_width
