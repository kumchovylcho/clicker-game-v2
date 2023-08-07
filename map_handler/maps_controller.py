from . import helpers
import settings
from map_handler.map import Map
from map_handler.platform import Platform


class MapsController:

    def __init__(self):
        self.maps = []
        self.current_map = 0

    @property
    def get_current_map(self):
        return self.maps[self.current_map]

    @property
    def get_platform(self):
        return self.get_current_map.platform

    @property
    def get_current_monster(self):
        return self.get_current_map.monsters[self.get_current_map.current_monster_index]

    def display_map_with_platform_and_monster(self, screen):
        screen.blits(blit_sequence=((self.get_current_map.background_img, (0, 0)),
                                    (self.get_platform.img, self.get_platform.get_position),
                                    (self.get_current_monster.image, self.get_platform.get_monster_position),
                                    ))

    @staticmethod
    def generate_initial_monsters_health():
        initial_health = settings.monster_initial_health
        result = {}

        # dynamically getting the number of maps
        for i in range(len(helpers.get_all_map_names())):
            result[i] = []

            # dynamically getting the number of monsters on map
            for _ in range(helpers.get_number_of_monsters_on_every_map()):
                result[i].append(initial_health)
                initial_health = round(initial_health * settings.monster_health_scale_value)

        return result

    def add_maps(self):
        map_names = helpers.get_all_map_names()
        map_backgrounds = helpers.get_map_images()
        bridge_to_platform = helpers.get_bridge_to_platforms()
        platform_positions = helpers.get_platform_positions()

        for map_name, map_bg in zip(map_names, map_backgrounds):
            platform_x, platform_y = platform_positions[map_name]["platform_pos"]
            monster_x, monster_y = platform_positions[map_name]["monster_pos"]

            new_platform = Platform(img=bridge_to_platform[map_name],
                                    x_pos=platform_x,
                                    y_pos=platform_y,
                                    monster_x=monster_x,
                                    monster_y=monster_y
                                    )
            new_map = Map(background_img=map_bg,
                          platform=new_platform
                          )
            monsters_for_map = helpers.get_monsters_on_chosen_map(map_name)
            new_map.add_monsters(monsters_for_map)

            self.maps.append(new_map)

    def set_monsters_initial_health(self):
        maps_with_monsters_health = self.generate_initial_monsters_health()
        for i in range(len(self.maps)):
            monsters_health = maps_with_monsters_health[i]
            for j in range(len(monsters_health)):
                self.maps[i].monsters[j].health = monsters_health[j]
