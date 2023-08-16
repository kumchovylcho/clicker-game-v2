import pygame
from helpers import create_font

TRANSPARENT = (0, 0, 0, 1)


class Shop:
    def __init__(self):
        pass

    def draw_background(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 100), (0, 200, 350, 600), border_radius=15)
        screen.blit(overlay, (0, 0))

    def draw_text(self, screen, x, y, text, color=(255, 255, 255)):
        fnt = create_font(text, "Georgia", 20, color, True)
        screen.blit(fnt, (x, y))

    def draw_button(self, screen, x, y, width, height, text):
        pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        fnt = create_font(text, "Georgia", 20, (0, 0, 0), True)

        text_width, text_height = fnt.get_size()
        text_x = x + (width - text_width) / 2
        text_y = y + (height - text_height) / 2

        screen.blit(fnt, (text_x, text_y))

    def check_for_collide(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def check_coins(self):
        pass

# 900 x 800
