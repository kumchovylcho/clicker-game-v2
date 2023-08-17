import pygame
from helpers import create_font


class Shop:
    def __init__(self):
        self.player_gold = None
        self.click_power_price = 100
        self.auto_clicker_price = 500

        self.can_update_click_power = False
        self.can_purchase_auto_clicker = False

    def draw_background(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 100), (0, 200, 350, 600), border_radius=15)
        screen.blit(overlay, (0, 0))

    def draw_text(self, screen, x, y, text, color=(255, 255, 255)):
        fnt = create_font(text, "Georgia", 20, color, True)
        screen.blit(fnt, (x, y))

    def draw_button(self, screen, x, y, width, height, text, price):
        if self.player_gold >= price:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)

        print(self.player_gold)
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
        fnt = create_font(text, "Georgia", 20, (0, 0, 0), True)

        text_width, text_height = fnt.get_size()
        text_x = x + (width - text_width) / 2
        text_y = y + (height - text_height) / 2

        screen.blit(fnt, (text_x, text_y))

    def check_for_collide(self, mouse_pos, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        return rect.collidepoint(mouse_pos)

    def check_coins_for_click_power_update(self, gold):
        if gold >= self.click_power_price:
            self.can_update_click_power = True
        else:
            self.can_update_click_power = False

    def check_coins_for_auto_clicker_purchase(self, gold):
        if gold >= self.auto_clicker_price:
            self.can_purchase_auto_clicker = True
        else:
            self.can_purchase_auto_clicker = False
