import pygame as pg
from button import Button
from coin_looper import CoinRotater
from helpers import get_screen_size
import settings
from menu import Menu
from sound import Sound
from map_handler.maps_controller import MapsController

pg.init()

pg.mouse.set_visible(False)

screen = pg.display.set_mode(get_screen_size())

clock = pg.time.Clock()

background = pg.image.load("images/menu/start_screen.jpg").convert_alpha()
cursor = pg.image.load("images/cursor/cursor.png").convert_alpha()

pg.display.set_icon(cursor)
pg.display.set_caption("Clicker Forever")

quit_button = Button((100, 40, 0), (180, 180, 180), (350, 400, 220, 70))
quit_button.default_button_construction("Quit", "Georgia", 50, (255, 255, 255), True, True)
settings_button = Button((100, 40, 0), (180, 180, 180), (350, 250, 220, 70))
settings_button.default_button_construction("Start", "Georgia", 50, (255, 255, 255), True, True)
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

maps_handler = MapsController()
maps_handler.add_maps()
maps_handler.set_monsters_initial_health()

game_running = True
while game_running:
    clock.tick(settings.GAME_FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            left_clicked = pg.mouse.get_pressed()[0]
            if left_clicked:
                sound_button.turn_off_on()

        elif event.type == pg.MOUSEBUTTONUP:
            pass

    screen.blit(background, (0, 0))
    maps_handler.display_map_with_platform_and_monster(screen)

    coin_looper.rotate_coin(screen)

    mouse_position = pg.mouse.get_pos()

    settings_button.if_the_courser_is_above_the_button(mouse_position, screen)
    quit_button.if_the_courser_is_above_the_button(mouse_position, screen)

    sound_button.display_image(screen)

    screen.blit(cursor, mouse_position)
    pg.display.update()

pg.quit()
