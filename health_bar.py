import pygame as pg


class HealthBar:

    def __init__(self,
                 x: float,
                 y: float,
                 width: float,
                 height: float,
                 color: tuple,
                 border_radius=10):

        self.max_width = width
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border_radius = border_radius

    def draw(self, screen):
        pg.draw.rect(screen,
                     self.color,
                     self.rect,
                     border_radius=self.border_radius,
                     )

    def lower_bar_width(self, current_health: float, max_health: float, remove_health: float):
        new_width = self.max_width * ((current_health - remove_health) / max_health)

        if new_width < 0:
            self.rect.width = 0

        elif new_width >= 0:
            self.rect.width = new_width