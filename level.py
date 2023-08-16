from pygame import Rect, draw

import helpers


class LevelDisplayer:

    def __init__(self,
                 x: float,
                 y: float,
                 width: float,
                 height: float,
                 color: tuple,
                 border_radius=6
                 ):
        self.border_radius = border_radius
        self.color = color
        self.rect = Rect(x, y, width, height)
        self.level = 1

        self.level_surface = self.level_surface_creator()

    def level_surface_creator(self):
        return helpers.create_font(value=f"Lv: {self.level}",
                                   font="Georgia",
                                   size_font=self.rect.height - 5,
                                   colour=(255, 255, 255),
                                   ).convert_alpha()

    def display_level(self, screen):
        draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

        center_x = helpers.calculate_center(self.rect.width, self.level_surface.get_width()) + self.rect.x
        center_y = helpers.calculate_center(self.rect.height, self.level_surface.get_height()) + self.rect.y

        screen.blit(self.level_surface, (center_x, center_y))

    def increase_level(self):
        self.level += 1

        self.level_surface = self.level_surface_creator()
