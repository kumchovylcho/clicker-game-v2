from pygame import Surface


class Platform:

    def __init__(self,
                 img: Surface,
                 x_pos: int,
                 y_pos: int,
                 monster_x: int,
                 monster_y: int):
        self.img = img
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.monster_x = monster_x
        self.monster_y = monster_y

    @property
    def get_platform_position(self):
        return self.x_pos, self.y_pos

    @property
    def get_monster_position(self):
        return self.monster_x, self.monster_y

