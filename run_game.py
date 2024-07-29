import pygame as pg

from companion import Companion
from level import LevelDisplayer
from shop_in_game import Shop
from text import Text
import settings

pg.init()
screen = pg.display.set_mode(settings.SCREEN_SIZE)

from button import Button
from coin_looper import CoinRotater
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

bird_images = [pg.image.load(f"images/companions/bird/bird{i}.png").convert_alpha() for i in range(1, 14)]
fireball_images = [pg.image.load(f"images/fireball/fb{i}.png").convert_alpha() for i in range(6)]
bird = Companion(bird_images=bird_images,
                 fireball_images=fireball_images,
                 damage=10,
                 )

level = LevelDisplayer(x=650, y=0, width=250, height=50, color=(0, 128, 255))
player = Player()
maps_handler = MapsController(player, level, bird)
maps_handler.add_maps()
maps_handler.set_monsters_initial_health_and_gold()

shop = Shop()
shop.add_texts([
    Text(
        settings.MENU_INCREASE_DAMAGE_TEXT_POSITION[1],
        f"{settings.MENU_INCREASE_DAMAGE_TEXT}1",
        settings.MENU_INCREASE_DAMAGE_TEXT_FONT,
        settings.MENU_INCREASE_DAMAGE_TEXT_FONT_SIZE,
        settings.MENU_INCREASE_DAMAGE_TEXT_COLOR,
        settings.MENU_OVERLAY_WIDTH,
        settings.MENU_OVERLAY_POSITION[0],
        settings.MENU_DAMAGE_TEXT_ID
    ),
    Text(
        settings.MENU_COMPANION_TEXT_POSITION[1],
        settings.MENU_COMPANION_TEXT,
        settings.MENU_COMPANION_TEXT_FONT,
        settings.MENU_COMPANION_TEXT_FONT_SIZE,
        settings.MENU_COMPANION_TEXT_COLOR,
        settings.MENU_OVERLAY_WIDTH,
        settings.MENU_OVERLAY_POSITION[0],
        settings.MENU_COMPANION_TEXT_ID
    ),
    Text(
        settings.MENU_COMPANION_LEVEL_TEXT_POSITION[1],
        settings.MENU_COMPANION_LEVEL_TEXT,
        settings.MENU_COMPANION_LEVEL_TEXT_FONT,
        settings.MENU_COMPANION_LEVEL_TEXT_FONT_SIZE,
        settings.MENU_COMPANION_LEVEL_TEXT_COLOR,
        settings.MENU_OVERLAY_WIDTH,
        settings.MENU_OVERLAY_POSITION[0],
        settings.MENU_COMPANION_LEVEL_TEXT_ID
    )
])

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
                maps_handler.attack_monster(mouse_pos=mouse_pos, player_dmg=True)
                maps_handler.player.switch_attack_state()

            if menu.is_opened and settings_button.check_collision(mouse_pos):
                menu.is_opened = False

            if menu.is_opened and quit_button.check_collision(mouse_pos):
                game_running = False

            if shop.can_update_click_power:
                if shop.check_for_collide(mouse_pos, 75, 300, 200, 70):
                    player.reduce_gold(shop.click_power_price)
                    player.increase_click_damage()
                    shop.increase_click_price()

            if shop.can_purchase_companion:
                if shop.check_for_collide(mouse_pos, 75, 500, 200, 70):
                    player.reduce_gold(shop.companion_price)
                    shop.is_companion_bought = True
                    shop.increase_companion_price()
                    maps_handler.bird_spawned = True
                    if shop.first_time_bought:
                        shop.first_time_bought = False
                    else:
                        maps_handler.bird.increase_damage(100)

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
    maps_handler.render_bird(screen=screen, mouse_pos=mouse_position)

    coin_looper.rotate_coin(screen)

    sound_button.display_image(screen)

    shop.player_gold = player.gold

    shop.render_overlay(screen)
    shop.render_texts(screen)

    shop.draw_button(screen, 75, 300, 200, 70,
                     f"coins: ",
                     shop.click_power_price)

    shop.draw_button(screen, 75, 500, 200, 70,
                     f"coins: ",
                     shop.companion_price)

    shop.check_coins_for_click_power_update(player.gold)
    shop.check_coins_for_companion(player.gold)

    screen.blit(cursor, mouse_position)

    pg.display.update()

pg.quit()
