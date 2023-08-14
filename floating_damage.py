import helpers


class FloatingDamage:

    def __init__(self,
                 damage: float,
                 mouse_x: float,
                 monster_y: float):
        self.damage = f"-{helpers.numbers_format(num=damage)}"

        self.damage_surface = helpers.create_font(value=self.damage,
                                                  font="Georgia",
                                                  size_font=70,
                                                  colour=(255, 0, 0),
                                                  )

        self.damage_shadow = helpers.create_font(value=self.damage,
                                                 font="Georgia",
                                                 size_font=70,
                                                 colour=(0, 0, 0),
                                                 )

        self.damage_position = [mouse_x, monster_y - 60]
        self.shadow_offset_position = [mouse_x + 3, monster_y - 60 + 3]

        self.float_speed = 4
        self.remove_alpha = 6
        self.alpha = 255

    @property
    def is_faded(self):
        return self.alpha < 0

    def move_damage_up(self):
        self.damage_position[1] -= self.float_speed
        self.shadow_offset_position[1] -= self.float_speed

    def float(self):
        self.move_damage_up()
        self.alpha -= self.remove_alpha

        if self.is_faded:
            return

        self.damage_shadow.set_alpha(self.alpha)
        self.damage_surface.set_alpha(self.alpha)

    def display_damage(self, screen):
        screen.blit(self.damage_shadow, self.shadow_offset_position)
        screen.blit(self.damage_surface, self.damage_position)
