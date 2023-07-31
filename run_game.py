import pygame
from button import Button

pygame.init()

width = 900
height = 800
screen = pygame.display.set_mode((width, height))
gameOn = True
background = pygame.image.load("images/menu/start_screen.jpg")


quit_button = Button((100, 40, 0), (180, 180, 180), (350, 400, 220, 70))
quit_button.default_button_construction("Quit", "Georgia", 50, (255, 255, 255), True, True)
settings_button = Button((100, 40, 0), (180, 180, 180), (350, 250, 220, 70))
settings_button.default_button_construction("Settings", "Georgia", 50, (255, 255, 255), True, True)


while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False

    screen.blit(background, (0, 0))

    mouse_position = pygame.mouse.get_pos()

    settings_button.if_the_courser_is_above_the_button(mouse_position, screen)
    quit_button.if_the_courser_is_above_the_button(mouse_position, screen)

    pygame.display.update()