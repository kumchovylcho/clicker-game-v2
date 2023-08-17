import pygame as pg
from helpers import get_screen_size
from level import LevelDisplayer
from shop_in_game import Shop

pg.init()
screen = pg.display.set_mode(get_screen_size())

from button import Button
from coin_looper import CoinRotater
import settings
from menu import Menu
from player import Player
from sound import Sound
from map_handler.maps_controller import MapsController

pg.mouse.set_visible(False)

clock = pg.time.Clock()

background = pg.image.load("images/menu/start_screen.jpg").convert_alpha()
cursor = pg.image.load("images/cursor/cursor.png").convert_alpha()

pg.display.set_icon(cursor)
pg.display.set_caption("Clicker Forever")

quit_button = Button((100, 0, 0), (180, 180, 180), (350, 400, 250, 90))
quit_button.center_button(900, 800 + 150)
quit_button.default_button_construction(
    "Quit",
    "Georgia",
    50,
    (255, 255, 255),
    True,
    True
)
settings_button = Button((0, 100, 0), (180, 180, 180), (350, 220, 250, 90))
settings_button.center_button(900, 800 - 150)

settings_button.default_button_construction(
    "Start",
    "Georgia",
    50,
    (255, 255, 255),
    True,
    True
)

sound_on = pg.image.load("images/sound/sound_on.png").convert_alpha()
sound_off = pg.image.load("images/sound/sound_off.png").convert_alpha()
sound_button = Sound(800, 700, sound_on, sound_off)

menu = Menu()
menu.add_buttons(quit_button, settings_button, sound_button)

coin_images = [pg.image.load(f"images/coins/coin_{i}.png").convert_alpha() for i in range(10)]
coin_looper = CoinRotater(coin_x=10,
                          coin_y=10,
                          images=coin_images
                          )

level = LevelDisplayer(x=650, y=0, width=250, height=50, color=(0, 128, 255))
player = Player()
maps_handler = MapsController(player, level)
maps_handler.add_maps()
maps_handler.set_monsters_initial_health_and_gold()

shop = Shop()

game_running = True
while game_running:
    clock.tick(settings.GAME_FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            left_click = pg.mouse.get_pressed()[0]
            mouse_pos = pg.mouse.get_pos()

            if left_click:
                sound_button.turn_off_on()

            if not maps_handler.player.is_attacking and left_click and maps_handler.is_collide(mouse_pos):
                maps_handler.attack_monster(mouse_pos=mouse_pos)
                maps_handler.player.switch_attack_state()

            if menu.is_opened and settings_button.check_collision(mouse_pos):
                menu.is_opened = False

            if menu.is_opened and quit_button.check_collision(mouse_pos):
                game_running = False

            if shop.can_update_click_power:
                if shop.check_for_collide(mouse_pos, 100, 300, 100, 50):
                    player.reduce_gold(shop.click_power_price)
                    shop.click_power_price += 50

            if shop.can_purchase_auto_clicker:
                if shop.check_for_collide(mouse_pos, 100, 450, 100, 50):
                    player.reduce_gold(shop.auto_clicker_price)
                    shop.auto_clicker_price += 500

        elif event.type == pg.MOUSEBUTTONUP:
            if maps_handler.player.is_attacking:
                maps_handler.player.switch_attack_state()

    screen.blit(background, (0, 0))
    mouse_position = pg.mouse.get_pos()
    sound_button.display_image(screen)

    if menu.is_opened:
        settings_button.if_the_courser_is_above_the_button(mouse_position, screen)
        quit_button.if_the_courser_is_above_the_button(mouse_position, screen)
        screen.blit(cursor, mouse_position)

        pg.display.flip()
        continue

    maps_handler.display_map_with_platform_and_monster(screen=screen)
    maps_handler.display_coin_animation(screen=screen)
    maps_handler.display_float_damage(screen=screen)
    maps_handler.display_reached_level(screen=screen)

    coin_looper.rotate_coin(screen)

    sound_button.display_image(screen)  # bug sled kato igrata startira butona izchezva

    shop.player_gold = player.gold

    shop.draw_background(screen)

    shop.draw_text(screen, 40, 260,
                   f"Increase click damage DAMAGE LEVEL")

    shop.draw_button(screen, 100, 300, 100, 50,
                     f"{shop.click_power_price} coins", 100)

    shop.draw_text(screen, 85, 410,
                   "Auto clicker LEVEL")
    shop.draw_button(screen, 100, 450, 100, 50,
                     f"{shop.auto_clicker_price} coins", 500)

    shop.check_coins_for_click_power_update(player.gold)
    shop.check_coins_for_auto_clicker_purchase(player.gold)

    screen.blit(cursor, mouse_position)

    pg.display.update()

pg.quit()
