import pygame


class Sound(pygame.sprite.Sprite):

    def __init__(self, x, y, sound_on, sound_off):
        super(Sound, self).__init__()
        self.x_pos = x
        self.y_pos = y
        self.is_turned_on = True
        self.sound_on = sound_on
        self.sound_off = sound_off
        self.rect = sound_on.get_rect()
        self.rect.x, self.rect.y = self.x_pos, self.y_pos

    @property
    def get_image_position(self):
        return self.x_pos, self.y_pos

    def display_image(self, screen):
        screen.blit(self.get_image(), self.get_image_position)

    def get_image(self):
        if self.is_turned_on:
            return self.sound_on
        else:
            return self.sound_off

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.is_turned_on and pygame.mouse.get_pressed()[0]:
                self.is_turned_on = False
            elif pygame.mouse.get_pressed()[0]:
                self.is_turned_on = True
        return self.is_turned_on

    def turn_off_on(self):
        if self.draw():
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.pause()