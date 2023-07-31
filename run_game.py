import pygame as pg
from button import Button
from helpers import get_screen_size

pg.init()

pg.mouse.set_visible(False)

screen = pg.display.set_mode(get_screen_size())

background = pg.image.load("images/menu/start_screen.jpg").convert_alpha()
cursor = pg.image.load("images/cursor/cursor.png").convert_alpha()


quit_button = Button((100, 40, 0), (180, 180, 180), (350, 400, 220, 70))
quit_button.default_button_construction("Quit", "Georgia", 50, (255, 255, 255), True, True)
settings_button = Button((100, 40, 0), (180, 180, 180), (350, 250, 220, 70))
settings_button.default_button_construction("Settings", "Georgia", 50, (255, 255, 255), True, True)

game_running = True
while game_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False

    screen.blit(background, (0, 0))

    mouse_position = pg.mouse.get_pos()

    settings_button.if_the_courser_is_above_the_button(mouse_position, screen)
    quit_button.if_the_courser_is_above_the_button(mouse_position, screen)

    screen.blit(cursor, mouse_position)
    pg.display.update()

pg.quit()