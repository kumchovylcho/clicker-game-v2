from helpers import create_font, calculate_center


class Text:

    def __init__(self,
                 y: int,
                 text: str,
                 font: str,
                 font_size: int,
                 text_color: tuple,
                 parent_container_width: int,
                 parent_container_x_pos: int,
                 text_id: int
                 ):
        self.text_obj = create_font(text, font, font_size, text_color)
        self.text_id = text_id

        self.parent_container_width = parent_container_width
        self.parent_container_x_pos = parent_container_x_pos
        self.x = calculate_center(self.parent_container_width, self.text_obj.get_width()) + self.parent_container_x_pos
        self.y = y
        self.font = font
        self.font_size = font_size
        self.text_color = text_color
        self.text = text

    def render_text(self, screen):
        screen.blit(self.text_obj, (self.x, self.y))

    def update_text(self, new_text: str):
        self.text_obj = create_font(new_text, self.font, self.font_size, self.text_color)
        self.recalculate_text_center()

    def recalculate_text_center(self):
        self.x = calculate_center(self.parent_container_width, self.text_obj.get_width()) + self.parent_container_x_pos