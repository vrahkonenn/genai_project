import random
from game_data import enemy_descriptions

class Enemy:
    def __init__(self, name, health, damage, ac):
        self.name = name
        self.health = health
        self.damage = damage
        self.ac = ac
        self.description = enemy_descriptions.get(name.lower(), {})
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health
    
    def is_dead(self):
        return self.health <= 0
    
    def attack(self, target):
        roll = random.randint(1,20)

        # Critical hit
        if roll == 20:
            dmg = self.damage * 2
            target.health -= dmg
            return {
                "roll": roll,
                "hit": True,
                "damage": dmg
            }

        # Critical miss
        if roll == 1:
            return {
                "roll": roll,
                "hit": False,
                "damage": 0
            }

        # Normal hit
        if roll > target.ac:
            dmg = self.damage
            target.health -= dmg
            return {
                "roll": roll,
                "hit": True,
                "damage": dmg
            }
        else:
            return {
                "roll": roll,
                "hit": False,
                "damage": 0
            }
