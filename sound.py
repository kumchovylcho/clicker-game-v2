import pygame as pg
import settings


class Sound:

    def __init__(self, x: int, y: int, sound_on: pg.Surface, sound_off: pg.Surface):
        self.x_pos = x
        self.y_pos = y
        self.is_turned_on = True
        self.sound_on = sound_on
        self.sound_off = sound_off
        self.rect = sound_on.get_rect()
        self.rect.x, self.rect.y = self.x_pos, self.y_pos

        self.sound_obj = pg.mixer.Sound('music/sound_of_menu/sound_for_menu.mp3')
        self.menu_music = pg.mixer.Channel(0)
        self.menu_music.play(self.sound_obj)
        self.menu_music.set_volume(settings.GAME_SOUND)

    @property
    def get_image_position(self):
        return self.x_pos, self.y_pos

    def display_image(self, screen):
        screen.blit(self.get_image(), self.get_image_position)

    def get_image(self):
        if self.is_turned_on:
            return self.sound_on
        return self.sound_off

    def check_button_state(self):
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.is_turned_on:
                self.is_turned_on = False
                self.pause_menu_music()

            elif not self.is_turned_on:
                self.is_turned_on = True
                self.unpause_menu_music()

    def pause_menu_music(self):
        self.menu_music.pause()

    def unpause_menu_music(self):
        self.menu_music.unpause()

    def turn_off_on(self):
        self.check_button_state()
