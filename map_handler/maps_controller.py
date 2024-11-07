from math import ceil

from collect_coins_animation import CollectCoins
from floating_damage import FloatingDamage
from . import helpers
import settings
from map_handler.map import Map
from map_handler.platform import Platform


class MapsController:

    def __init__(self, player, level_displayer, bird):
        self.player = player
        self.maps = []
        self.current_map = 0

        self.coin_collectors: list[CollectCoins] = []
        self.floating_damage: list[FloatingDamage] = []
        self.level_displayer = level_displayer

        self.bird = bird
        self.bird_spawned = False

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

    def render_bird(self, screen, mouse_pos: tuple):
        if not self.bird_spawned:
            return

        self.bird.render(screen=screen)

        if self.bird.fireball_reached():
            self.attack_monster(mouse_pos=mouse_pos,
                                companion_dmg=self.bird.damage
                                )
            self.bird.set_cooldown()
            self.bird.reset_fireball()

    def attack_monster(self, mouse_pos: tuple, companion_dmg=None, player_dmg=False):
        if companion_dmg:
            self.get_current_monster.take_damage(self.bird.damage)
            self.floating_damage.append(FloatingDamage(damage=self.bird.damage,
                                                       mouse_x=650,
                                                       monster_y=self.get_current_monster.y_pos
                                                       ))

        if player_dmg:
            self.get_current_monster.take_damage(self.player.click_damage)
            self.floating_damage.append(FloatingDamage(damage=self.player.click_damage,
                                                       mouse_x=mouse_pos[0],
                                                       monster_y=self.get_current_monster.y_pos
                                                       ))

        if self.get_current_monster.is_dead:
            self.coin_collectors.append(CollectCoins(gold_reward=self.get_current_monster.give_reward(),
                                                     monster_x=self.get_current_monster.monster_pos[0],
                                                     monster_y=self.get_current_monster.monster_pos[1],
                                                     monster_height=self.get_current_monster.rect.height,
                                                     ))

            self.get_current_monster.prepare_for_next_spawn_after_death()
            self.level_displayer.increase_level()

            if self.get_current_map.is_last_monster:
                self.get_current_map.reset_monster_index()
                self.switch_next_map()

            elif not self.get_current_map.is_last_monster:
                self.get_current_map.spawn_next_monster()

    def display_coin_animation(self, screen):
        not_collected_coins = []
        for collector in self.coin_collectors:
            collector.display_coins(screen)
            collector.drop_animation()
            collector.collect_coins(player=self.player)

            if collector.coins:
                not_collected_coins.append(collector)

        self.coin_collectors = not_collected_coins

    def display_float_damage(self, screen):
        not_faded_damage = []
        for damage in self.floating_damage:
            damage.render(screen)

            if not damage.is_faded:
                not_faded_damage.append(damage)

        self.floating_damage = not_faded_damage

    def display_reached_level(self, screen):
        self.level_displayer.display_level(screen=screen)

    def is_collide(self, mouse_pos: tuple[int, int]) -> bool:
        return self.get_current_monster.rect.collidepoint(mouse_pos)
