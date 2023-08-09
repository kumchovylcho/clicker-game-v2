from button import Button


class Menu:

    def __init__(self):
        self.buttons: list = []

    def add_buttons(self, *buttons):
        for button in buttons:
            self.buttons.append(button)