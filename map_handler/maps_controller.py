from math import ceil

from collect_coins_animation import CollectCoins
from . import helpers
import settings
from map_handler.map import Map
from map_handler.platform import Platform


class MapsController:

    def __init__(self, player):
        self.player = player
        self.maps = []
        self.current_map = 0

        self.coin_collectors: list[CollectCoins] = []

    @property
    def get_current_map(self):
        return self.maps[self.current_map]

    @property
    def get_platform(self):
        return self.get_current_map.platform

    @property
    def get_current_monster(self):
        index = self.get_current_map.current_monster_index
        return self.get_current_map.monsters[index]

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
                initial_health = ceil(initial_health * settings.monster_health_scale_value)

        return result

    @staticmethod
    def generate_initial_monster_gold_rewards():
        initial_gold = settings.monster_initial_gold_reward
        result = {}

        # dynamically getting the number of maps
        for i in range(len(helpers.get_all_map_names())):
            result[i] = []

            # dynamically getting the number of monsters on map
            for _ in range(helpers.get_number_of_monsters_on_every_map()):
                result[i].append(initial_gold)
                initial_gold = ceil(initial_gold * settings.monster_initial_gold_reward_scale)

        return result

    def add_maps(self):
        map_names = helpers.get_all_map_names()
        map_backgrounds = helpers.get_map_images()
        bridge_to_platform = helpers.get_bridge_to_platforms()
        platform_positions = helpers.get_platform_positions()

        for map_name, map_bg in zip(map_names, map_backgrounds):
            platform_x, platform_y = platform_positions[map_name]

            new_platform = Platform(img=bridge_to_platform[map_name],
                                    x_pos=platform_x,
                                    y_pos=platform_y,
                                    )
            new_map = Map(background_img=map_bg,
                          platform=new_platform
                          )
            monsters_for_map = helpers.get_monsters_on_chosen_map(map_name)
            new_map.add_monsters(monsters_for_map)

            self.maps.append(new_map)

    def set_monsters_initial_health_and_gold(self):
        maps_with_monsters_health = self.generate_initial_monsters_health()
        maps_with_monsters_gold_reward = self.generate_initial_monster_gold_rewards()

        for i in range(len(self.maps)):
            monsters_health = maps_with_monsters_health[i]
            monsters_gold_reward = maps_with_monsters_gold_reward[i]

            for j in range(len(monsters_health)):
                settings.last_monster_health = monsters_health[j]
                settings.last_monster_gold_reward = monsters_gold_reward[j]

                self.maps[i].monsters[j].gold_reward = monsters_gold_reward[j]
                self.maps[i].monsters[j].health = monsters_health[j]
                self.maps[i].monsters[j].set_max_health(monsters_health[j])
                self.maps[i].monsters[j].gold_reward = settings.last_monster_gold_reward

    def switch_next_map(self):
        self.current_map += 1

        if self.current_map >= len(self.maps):
            self.current_map = 0

    def display_map_with_platform_and_monster(self, screen):
        screen.blits(blit_sequence=((self.get_current_map.background_img, (0, 0)),
                                    (self.get_platform.img, self.get_platform.get_position),
                                    (self.get_current_monster.image, self.get_current_monster.monster_pos),
                                    (self.player.gold_surface, self.player.gold_position),
                                    ))

        self.get_current_monster.health_bar_pad.draw(screen)
        self.get_current_monster.health_bar.draw(screen)

        screen.blit(*self.get_current_monster.prepare_text_for_display())

    def attack_monster(self):
        #self.get_current_monster.take_damage(self.player.click_damage)
        self.get_current_monster.take_damage(5000)

        if self.get_current_map.is_last_monster and self.get_current_monster.is_dead:
            self.add_collector(self.get_current_monster.give_reward(),
                               self.get_current_monster.monster_pos[0],
                               self.get_current_monster.monster_pos[1],
                               self.get_current_monster.rect.height,
                               )
            self.get_current_monster.prepare_for_next_spawn_after_death()
            self.get_current_map.spawn_next_monster()
            self.switch_next_map()

        if not self.get_current_map.is_last_monster and self.get_current_monster.is_dead:
            self.add_collector(self.get_current_monster.give_reward(),
                               self.get_current_monster.monster_pos[0],
                               self.get_current_monster.monster_pos[1],
                               self.get_current_monster.rect.height,
                               )
            self.get_current_monster.prepare_for_next_spawn_after_death()
            self.get_current_map.spawn_next_monster()

    def add_collector(self, reward: int, monster_x: float, monster_y: float, monster_height: float):
        self.coin_collectors.append(CollectCoins(gold_reward=reward,
                                                 monster_x=monster_x,
                                                 monster_y=monster_y,
                                                 monster_height=monster_height,
                                                 ))

    def display_coin_animation(self, screen):
        for collector in self.coin_collectors:
            collector.display_coins(screen)
            collector.drop_animation()
            collector.collect_coins(player=self.player)

        self.clear_coin_collectors()

    def clear_coin_collectors(self):
        if self.coin_collectors:
            self.coin_collectors = [c for c in self.coin_collectors if c.coins]

    def is_collide(self, mouse_pos: tuple[int, int]) -> bool:
        return self.get_current_monster.rect.collidepoint(mouse_pos)
