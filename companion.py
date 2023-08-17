from math import (atan2,
                  cos,
                  sin,
                  degrees
                  )
from typing import Sequence

from pygame import (Surface,
                    transform
                    )
import settings


class Companion:

    def __init__(self,
                 bird_images: Sequence[Surface],
                 fireball_images: Sequence[Surface],
                 damage: int,
                 companion_x=350,
                 companion_y=620):
        self.damage = damage
        self.companion_x = companion_x
        self.companion_y = companion_y

        self.bird_images = bird_images
        self.bird_index = 0
        self.bird_loop_speed = 0.28

        self.fireball_images = fireball_images
        self.fireball_rect = self.fireball_images[0].get_rect()
        self.fireball_rect.x, self.fireball_rect.y = self.fireball_start_pos
        self.fireball_index = 0
        self.fireball_loop_speed = 0.15
        self.fireball_fly_speed = 3

        self.alpha = 0
        self.spawn_speed = 4
        self.shoot_cooldown = 0
        self.cooldown = 1.3

        self.direction = atan2(self.fireball_end_pos[1] - self.fireball_start_pos[1],
                               self.fireball_end_pos[0] - self.fireball_start_pos[0])

    @property
    def fireball_start_pos(self):
        return 480, 710

    @property
    def fireball_end_pos(self):
        return 650, 420

    @property
    def can_attack(self):
        return self.shoot_cooldown <= 0

    @property
    def is_spawned(self):
        return self.alpha >= 255

    @property
    def companion_img(self):
        if self.is_spawned:
            index = int(self.bird_index)
            return self.bird_images[index]
        return self.bird_images[0]

    def fireball_reached(self):
        return self.fireball_rect.x >= self.fireball_end_pos[0] and \
            self.fireball_rect.y >= self.fireball_end_pos[1]

    def lower_cooldown(self):
        self.shoot_cooldown -= 1 / settings.GAME_FPS

    def spawn(self):
        self.alpha += self.spawn_speed
        if self.is_spawned:
            self.alpha = 255

        self.bird_images[0].set_alpha(self.alpha)

    def increase_damage(self, amount: int):
        self.damage += amount

    def reset_fireball(self):
        self.fireball_rect.x, self.fireball_rect.y = self.fireball_start_pos
        self.fireball_index = 0

    def set_cooldown(self):
        self.shoot_cooldown = self.cooldown

    def render(self, screen):
        screen.blit(self.companion_img, (self.companion_x, self.companion_y))
        if not self.is_spawned:
            self.spawn()
            return

        self.bird_index += self.bird_loop_speed
        if self.bird_index >= len(self.bird_images):
            self.bird_index = 0

        if not self.can_attack:
            self.lower_cooldown()
            if self.shoot_cooldown <= 0:
                self.shoot_cooldown = 0

        elif self.can_attack and not self.fireball_reached():

            self.fireball_rect.x += self.fireball_fly_speed * cos(self.direction)
            self.fireball_rect.y += self.fireball_fly_speed * sin(self.direction)

            self.fireball_index += self.fireball_loop_speed
            if self.fireball_index >= len(self.fireball_images):
                self.fireball_index = 0

            fireball = transform.rotate(surface=self.fireball_images[int(self.fireball_index)],
                                        angle=degrees(abs(self.direction))
                                        )
            screen.blit(fireball, (self.fireball_rect.x, self.fireball_rect.y))
