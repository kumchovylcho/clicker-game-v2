from pygame import Surface


class Platform:

    def __init__(self,
                 img: Surface,
                 x_pos: int,
                 y_pos: int):
        self.img = img
        self.x_pos = x_pos
        self.y_pos = y_pos

    @property
    def get_position(self):
        return self.x_pos, self.y_pos
