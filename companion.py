from typing import Sequence

from pygame import Surface, Rect


class Companion:

    def __init__(self,
                 bird_images: Sequence[Surface],
                 fireball_images: Sequence[Surface],
                 damage: int,
                 monster_rect: Rect,
                 companion_x=350,
                 companion_y=620):
        self.damage = damage
        self.companion_x = companion_x
        self.companion_y = companion_y
        self.monster_rect = monster_rect

        self.bird_images = bird_images
        self.bird_index = 0
        self.bird_loop_speed = 0.28

        self.fireball_images = fireball_images
        self.fireball_index = 0
        self.fireball_loop_speed = 0.15

        self.alpha = 0
        self.spawn_speed = 4
        self.shoot_cooldown = 0
        self.cooldown = 1.3

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

    def spawn(self):
        self.alpha += self.spawn_speed
        if self.is_spawned:
            self.alpha = 255

        self.bird_images[0].set_alpha(self.alpha)

    def increase_damage(self, amount: int):
        self.damage += amount

    def render(self, screen):
        screen.blit(self.companion_img, (self.companion_x, self.companion_y))
        if not self.is_spawned:
            self.spawn()
            return

        self.bird_index += self.bird_loop_speed
        if self.bird_index >= len(self.bird_images):
            self.bird_index = 0


