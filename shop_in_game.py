import math

import pygame
from helpers import create_font, numbers_format


class Shop:
    def __init__(self):
        self.player_gold = None
        self.click_power_price = 1
        self.click_power_level = 1

        self.companion_price = 0
        self.is_companion_bought = False

        self.can_update_click_power = False
        self.can_purchase_companion = False
        self.first_time_bought = True

        self.companion_level = 0

    def draw_background(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 100), (0, 200, 350, 600), border_radius=15)
        screen.blit(overlay, (0, 0))

    def draw_text(self, screen, x, y, text, color=(255, 255, 255)):
        fnt = create_font(text, "Georgia", 20, color, True)
        screen.blit(fnt, (x, y))

    def draw_text_companion(self, screen, x, y, text, color=(255, 255, 255)):
        fnt = create_font(text, "Georgia", 27, color, True)
        screen.blit(fnt, (x, y))

    def draw_button(self, screen, x, y, width, height, text, price):
        color = (160, 160, 160)
        if self.player_gold >= price:
            color = (0, 255, 0)

        formatted_cost = numbers_format(price)
        new_text = text + formatted_cost

        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
        fnt = create_font(new_text, "Georgia", 20, (0, 0, 0), True)

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

    def check_coins_for_companion(self, gold):
        if gold >= self.companion_price:
            self.can_purchase_companion = True
        else:
            self.can_purchase_companion = False

    def increase_click_price(self):
        self.click_power_price = math.ceil(self.click_power_price * 1.05)

    def increase_companion_price(self):
        self.companion_price = math.ceil(self.companion_price * 1.1)
