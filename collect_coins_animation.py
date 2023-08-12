from math import (atan2,
                  cos,
                  sin,
                  )
from random import randint
from pygame import image


class CollectCoins:
    coin_img = image.load("images/coins/coin_0.png").convert_alpha()

    def __init__(self,
                 gold_reward: int,
                 monster_x: float,
                 monster_y: float,
                 monster_height: float):

        self.gold_reward = gold_reward
        self.how_many_coins = self.get_random_number_of_coins
        self.coins = self.distribute_coins()

        self.monster_x = monster_x
        self.monster_y = monster_y
        self.monster_height = monster_height

        self.coins_map = self.spawn_coins()

        self.drop_speed = 3
        self.bounce_speed = 1
        self.collect_speed = 8

    @property
    def get_random_number_of_coins(self):
        return randint(1, 4)

    @property
    def coins_storage_position(self):
        return 30, 20

    @property
    def coin_positions(self):
        return [(self.monster_x - 20, self.monster_y),
                (self.monster_x + 30, self.monster_y + 50),
                (self.monster_x + 80, self.monster_y + 20),
                (self.monster_x + 130, self.monster_y + 72),
                ]

    @property
    def drop_coin_end_position(self):
        return self.monster_y + self.monster_height - 40

    @property
    def bounce_height(self):
        return 30

    def distribute_coins(self):
        coins_per_target = self.gold_reward // self.how_many_coins
        remainder = self.gold_reward % self.how_many_coins

        coins_distribution = [coins_per_target] * self.how_many_coins
        for i in range(remainder):
            coins_distribution[i] += 1

        return coins_distribution

    @staticmethod
    def calculate_direction(x1, y1, x2, y2):
        return atan2(y2 - y1, x2 - x1)

    def spawn_coins(self):
        result = []

        for x, y in self.coin_positions[:self.how_many_coins]:
            direction = self.calculate_direction(x,
                                                 self.drop_coin_end_position,
                                                 self.coins_storage_position[0],
                                                 self.coins_storage_position[1],
                                                 )

            result.append({self.coin_img: {"start": [x, y],
                                           "end": [x, self.drop_coin_end_position],
                                           "direction": direction,
                                           "bottom_reached": False,
                                           "bounce_reached": False,
                                           "static": False,
                                           "bounce": 0,
                                           }})

        return result

    def display_coins(self, screen):
        for coin in self.coins_map:
            for img, info in coin.items():
                position = info['end']
                if not info['static']:
                    position = info['start']

                screen.blit(img, position)

    def drop_animation(self):
        for coin in self.coins_map:
            for img, info in coin.items():
                if not info['bottom_reached']:
                    info['start'][1] += self.drop_speed
                    if info['start'][1] >= info['end'][1]:
                        info['bottom_reached'] = True

                elif info['bottom_reached']:
                    if not info['bounce_reached']:
                        info['start'][1] += -self.bounce_speed
                        info['bounce'] += self.bounce_speed
                        if info['bounce'] >= self.bounce_height:
                            info['bounce_reached'] = True

                    elif info['bounce_reached']:
                        if info['bounce'] > 0:
                            info['bounce'] -= self.bounce_speed
                            info['start'][1] += self.bounce_speed

                if info['bottom_reached'] and info['bounce_reached'] and info['bounce'] <= 0:
                    info['static'] = True

    def collect_coins(self, player):
        if not self.coins:
            return

        for coin in self.coins_map:
            for img, info in coin.items():
                if not info['static']:
                    continue

                info['end'][0] += self.collect_speed * cos(info['direction'])
                info['end'][1] += self.collect_speed * sin(info['direction'])

                if info['end'][0] < self.coins_storage_position[0] and info['end'][1] < self.coins_storage_position[1]:
                    self.coins_map.remove(coin)
                    player.collect_loot(self.coins.pop())
