from helpers import create_font, calculate_center
import pygame


class Button:

    def __init__(self, button_colour: tuple, if_above_color: tuple, rect_size: tuple):
        self.button_colour = button_colour
        self.if_above_color = if_above_color
        self.rect = pygame.Rect(*rect_size)
        self.surf_button = None

    def check_if_hover(self, mouse_position: tuple) -> bool:
        return self.rect.collidepoint(mouse_position)

    def default_button_construction(self, value: str, font: str, size_font: int, colour: tuple, bold=True,
                                    antialias=True):
        self.surf_button = create_font(value, font, size_font, colour, bold, antialias)

    def if_the_courser_is_above_the_button(self, mouse_position: tuple, screen):
        colour_of_settings_button = self.button_colour
        if self.check_if_hover(mouse_position):
            colour_of_settings_button = self.if_above_color

        pygame.draw.rect(screen, colour_of_settings_button, self.rect, border_radius=30)

        calculate_x = calculate_center(self.rect.width, self.surf_button.get_width()) + self.rect.x
        calculate_y = calculate_center(self.rect.height, self.surf_button.get_height()) + self.rect.y

        screen.blit(self.surf_button, (calculate_x, calculate_y))

    def check_collision(self, mouse_position):
        return self.rect.collidepoint(mouse_position)

    def center_button(self, screen_width, screen_height):
        button_width = self.rect.width
        button_height = self.rect.height

        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2

        self.rect.topleft = (button_x, button_y)

