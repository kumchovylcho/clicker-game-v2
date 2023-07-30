import pygame

pygame.init()

width = 900
height = 800
screen = pygame.display.set_mode((width, height))
gameOn = True
background = pygame.image.load("images/menu/start_screen.jpg")

while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
    screen.blit(background, (0, 0))
    pygame.display.update()
