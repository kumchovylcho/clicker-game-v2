from button import Button


class Menu:

    def __init__(self):
        self.buttons: list = []
        self.is_opened = True  # menu on/off

    def add_buttons(self, *buttons):
        for button in buttons:
            self.buttons.append(button)

    def start_game(self):
        self.is_opened = False
