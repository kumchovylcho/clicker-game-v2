from helpers import create_font, calculate_center
import pygame


class Button:

    def __init__(self, button_colour: tuple, if_above_color: tuple, rect_size:tuple):
        self.button_colour = button_colour
        self.if_above_color = if_above_color
        self.rect = pygame.Rect(*rect_size)
        self.surf_button = None

    def check_if_hover(self, mouse_position:tuple) -> bool:
        return self.rect.collidepoint(mouse_position)

    def default_button_construction(self, value:str, font:str, size_font:int, colour: tuple, bold=True, antialias=True):
        self.surf_button = create_font(value, font, size_font, colour, bold, antialias)

    def if_the_courser_is_above_the_button(self, mouse_position:tuple, screen):
        colour_of_settings_button = self.button_colour
        if self.check_if_hover(mouse_position):
            colour_of_settings_button = self.if_above_color

        pygame.draw.rect(screen, colour_of_settings_button, self.rect)

        calculate_x = calculate_center(self.rect.width, self.surf_button.get_width()) + self.rect.x
        screen.blit(self.surf_button, (calculate_x, self.rect.y))
