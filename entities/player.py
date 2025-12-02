import random 

class Player:
    def __init__(self, name, health, inventory, ac):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.ac = ac

    def attack(self, target, weapon):
        # d20 Attack roll
        roll = random.randint(1,20)

        # Roll 20 osuu aina, 2x damage
        if roll == 20:
            base_dmg = self.inventory[weapon]["damage"]
            dmg = base_dmg * 2
            target.take_damage(dmg)
            return {
                "roll": roll,
                "hit": True,
                "damage": dmg,
                "weapon": weapon
            }
        
        # Roll 1 menee huti aina
        if roll == 1:
            return {
                "roll": roll,
                "hit": False,
                "damage": 0,
                "weapon": weapon
            }
        
        if roll > target.ac:
            dmg = self.inventory[weapon]["damage"]
            target.take_damage(dmg)
            return {
                "roll": roll,
                "hit": True,
                "damage": dmg,
                "weapon": weapon
            }
        else: 
            return {
                "roll": roll,
                "hit": False,
                "damage": 0,
                "weapon": weapon
        }