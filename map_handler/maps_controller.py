import helpers
from map_handler.map import Map
from map_handler.platform import Platform


class MapsController:

    def __init__(self):
        self.maps = []

    def add_maps(self):
        map_names = helpers.get_all_map_names()
        map_backgrounds = helpers.get_map_images()
        bridge_to_platform = helpers.get_bridge_to_platforms()

        for map_name, map_bg in zip(map_names, map_backgrounds):
            new_platform = Platform(img=bridge_to_platform[map_name],
                                    x_pos=300,
                                    y_pos=300,
                                    monster_x=300,
                                    monster_y=300
                                    )
            new_map = Map(background_img=map_bg,
                          platform=new_platform
                          )
            monsters_for_map = helpers.get_monsters_on_chosen_map(map_name)
            new_map.add_monsters(monsters_for_map)

            self.maps.append(new_map)

    def set_monsters_initial_health(self):
        pass

    def set_platform_positions(self):
        pass