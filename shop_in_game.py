import math

import pygame
from helpers import create_font, numbers_format
from text import Text
import settings


class Shop:
    def __init__(self):
        self.player_gold = None
        self.click_power_price = 1
        self.click_power_level = 1

        self.companion_price = 1000
        self.is_companion_bought = False

        self.can_update_click_power = False
        self.can_purchase_companion = False
        self.first_time_bought = True

        self.companion_level = 0

        self.menu_overlay = pygame.Surface(settings.SCREEN_SIZE, pygame.SRCALPHA)

        self.texts: [Text] = []

    def add_texts(self, texts: list[Text]):
        for text in texts:
            self.texts.append(text)

    def render_overlay(self, screen):
        pygame.draw.rect(self.menu_overlay,
                         settings.MENU_OVERLAY_COLOR,
                         (0, 0, settings.MENU_OVERLAY_WIDTH, settings.MENU_OVERLAY_HEIGHT),
                         border_radius=settings.MENU_OVERLAY_BORDER_RADIUS
                         )
        screen.blit(self.menu_overlay, settings.MENU_OVERLAY_POSITION)

    def render_texts(self, screen):
        for text in self.texts:
            if text.text_id == settings.MENU_COMPANION_LEVEL_TEXT_ID and self.companion_level == 0:
                continue

            text.render_text(screen)

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

    @staticmethod
    def check_for_collide(mouse_pos, x, y, width, height):
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
        self.click_power_level += 1
        for text in self.texts:
            if text.text_id != settings.MENU_DAMAGE_TEXT_ID:
                continue

            text.update_text(f"{settings.MENU_INCREASE_DAMAGE_TEXT}{self.click_power_level}")

    def increase_companion_price(self):
        self.companion_price = math.ceil(self.companion_price * 1.1)

        for text in self.texts:
            if text.text_id != settings.MENU_COMPANION_TEXT_ID:
                continue

            if text.text == settings.MENU_COMPANION_UPGRADE_TEXT:
                break

            text.update_text(settings.MENU_COMPANION_UPGRADE_TEXT)

        self.increase_companion_level()

    def increase_companion_level(self):
        self.companion_level += 1
        for text in self.texts:
            if text.text_id != settings.MENU_COMPANION_LEVEL_TEXT_ID:
                continue

            text.update_text(f"{settings.MENU_COMPANION_LEVEL_TEXT}{self.companion_level}")
