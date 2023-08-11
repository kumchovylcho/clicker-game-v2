import helpers


class Player:

    def __init__(self):
        self.is_attacking = False
        self.click_damage = 1
        self.gold = 0
        self.gold_surface = self.create_gold_surface()

    @property
    def gold_position(self):
        return 70, 15

    def create_gold_surface(self):
        formatted_gold = helpers.numbers_format(self.gold)
        return helpers.create_font(f"{formatted_gold}",
                                   "Georgia",
                                   30,
                                   (0, 0, 0)
                                   ).convert_alpha()

    def switch_attack_state(self):
        if not self.is_attacking:
            self.is_attacking = True

        elif self.is_attacking:
            self.is_attacking = False

    def collect_loot(self, amount: float):
        self.gold += amount
        self.gold_surface = self.create_gold_surface()

    def increase_click_damage(self):
        self.click_damage += 1
