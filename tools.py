from game_data import inventory, enemy_templates, player_start_stats, enemy_descriptions
from entities.player import Player
from entities.enemy import Enemy
import time
from states import battle_state, game_state, dialogue_state
from ai.generate_battle_texts import generate_battle_text, generate_enemy_battle_text




player = Player(
    **player_start_stats,
    inventory = inventory
)
'''
current_enemy = Enemy(
    "Goblini", **enemy_templates["goblin"]
)
'''


def typewriter(text: str, delay: float = 0.04):
    """Tulostaa tekstin kirjain kerrallaan näyttävästi."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # Rivinvaihto lopuksi
    time.sleep(1)


# --------------------------------------------------------------------------------------------------- 
# --------------------------------------------EXPLORATION-------------------------------------------- 
# ---------------------------------------------------------------------------------------------------

def start_dialogue_tool(npc_name: str):
    """
    Käynnistää dialogin NPC:n kanssa
    """

    if npc_name in enemy_descriptions:
        personality = enemy_descriptions[npc_name]["personality"]
    else:
        personality = "tavallinen"

    game_state["state"] = "DIALOGUE"
    dialogue_state["npc_name"] = npc_name
    dialogue_state["npc_personality"] = personality
    dialogue_state["history"] = []

    typewriter(f"💬 Aloitetaan keskustelu {npc_name} kanssa... 🗣️")

    return ""

start_dialogue_function = {
    "name": "start_dialogue",
    "description": "Start a dialogue with an NPC or Enemy the player is interacting with",
    "parameters": {
        "type": "object",
        "properties": {
            "npc_name": {
                "type": "string",
                "description": "NPC name, e.g. Beggar, Goblin, Blacksmith"
            }
        },
        "required": ["npc_name"]
    }
}

#------------------------------------------------------

def start_combat(enemy_name: str):
    game_state["state"] = "COMBAT"

    enemy_data = enemy_templates[enemy_name.lower()]

    if not enemy_data:
        return f"Tuntematon vihollinen: {enemy_name}"

    enemy = Enemy(enemy_name.capitalize(), **enemy_data)

    battle_state["player"] = player
    battle_state["enemies"] = [enemy]
    battle_state["history"] = ["Taistelu alkaa..."]

    typewriter(f"⚔️ Aloitetaan taistelu {enemy_name} kanssa... 🩸")
    return ''

start_combat_function = {
    "name": "start_combat",
    "description": "Start a combat against an enemy",
    "parameters": {
        "type": "object",
        "properties": {
            "enemy_name": {
                "type": "string",
                "description": "Enemy name, e.g. goblin, orc or skeleton"
            }
        },
        "required": ["enemy_name"]
    }
}

# --------------------------------------------------------------------------------------------------- 
# --------------------------------------------- COMBAT ---------------------------------------------- 
# ---------------------------------------------------------------------------------------------------

def attack_enemy(weapon: str):
    player = battle_state["player"]
    enemies = battle_state["enemies"]

    if not enemies:
        return "Ei vihollisia jäljellä."

    current_enemy = enemies[0]

    result = player.attack(current_enemy, weapon)

    if current_enemy.health <= 0:
        dies = True
    else:
        dies = False

    roll = result["roll"]
    hit = result["hit"]
    dmg = result["damage"]
    weapon = result["weapon"]

    typewriter(f"{player.name} valmistautuu hyökkäykseen...", 0.03)

    if roll == 20:
        typewriter("🎯🔥 KRIITTINEN OSUMA 2X DMG 🎯🔥", 0.02)

    ai_text = generate_battle_text(
        attacker="Pelaaja",
        target=current_enemy.name,
        target_health = current_enemy.health,
        weapon=weapon,
        roll=roll,
        hit=hit,
        damage=dmg,
        dies = dies,
        battle_state = battle_state
    )

    battle_state["history"].append(ai_text)

    print()
    typewriter(ai_text)
    print()

    if current_enemy.health <= 0:
        typewriter(f"💀 Vihollinen {current_enemy.name} kaatuu kuolleena maahan!\n")
        enemies.remove(current_enemy)
        game_state["state"]="EXPLORATION"
        return ""

    
    time.sleep(1)
    typewriter(f"🔁 {current_enemy.name} valmistautuu vastaiskuun...", 0.03)
    enemy_attack_player()
    
    if player.health <= 0:
        typewriter("💀 Olet kuollut!", 0.05)
        return ""

    print(f"{player.name} health: {player.health}❤️")
    print(f"{current_enemy.name} health: {current_enemy.health}❤️")
    return ""

attack_function = {
    "name": "attack_enemy",
    "description": "Player attacks enemy using a weapon",
    "parameters": {
        "type": "object",
        "properties": {
            "weapon": {
                "type": "string",
                "description": "The item name, e.g. axe"
            }
        },
        "required": ["weapon"]
    }
}


def enemy_attack_player():

    current_enemy = battle_state["enemies"][0]
    player = battle_state["player"]

    result = current_enemy.attack(player)

    roll = result["roll"]
    hit = result["hit"]
    dmg = result["damage"]

    if roll == 20:
        typewriter("🎯🔥 KRIITTINEN OSUMA 2X DMG 🎯🔥", 0.02)
        
    dies = player.health <= 0

    ai_text = generate_enemy_battle_text(
        attacker=current_enemy.name,
        target=player.name,
        target_health=player.health,
        roll=roll,
        hit=hit,
        damage=dmg,
        dies=dies,
        battle_state=battle_state,
        event_type="normal_attack"
    )

    battle_state["history"].append(ai_text)

    typewriter("\n" + ai_text + "\n")

    return ""

def flee_combat():
    """
    Pelaaja yrittää paeta taistelusta.
    Vihollinen saa yhden ilmaisen iskun.
    """

    enemies = battle_state["enemies"]
    enemy = enemies[0]

    typewriter(f"🏃 {player.name} yrittää paeta...", 0.03)
    time.sleep(0.5)
    typewriter(f"⚔️ {enemy.name} saa ilmaisen iskun!", 0.03)

    # Vihollisen ilmainen hyökkäys
    result = enemy.attack(player)

    roll = result["roll"]
    hit = result["hit"]
    dmg = result["damage"]

    if roll == 20:
        typewriter("🎯🔥 KRIITTINEN OSUMA PAKOYRITYKSEN AIKANA! 🔥🎯", 0.02)

    ai_text = generate_enemy_battle_text(
        attacker=enemy.name,
        target=player.name,
        target_health=player.health,
        roll=roll,
        hit=hit,
        damage=dmg,
        dies=player.health <= 0,
        battle_state=battle_state,
        event_type="flee_attack"
    )

    typewriter("\n" + ai_text + "\n")

    if player.health <= 0:
        typewriter("💀 Kuolit yrittäessäsi paeta.", 0.05)
        battle_state["active"] = False
        return ""

    # Pako onnistuu
    battle_state["player"] = None
    battle_state["enemies"] = []
    battle_state["history"] = []

    game_state["state"] = "EXPLORATION"

    typewriter("✅ Pääsit pakenemaan taistelusta!")
    return ""

flee_combat_function = {
    "name": "flee_combat",
    "description": "Attempt to flee from combat. Enemy gets a free attack.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}


# --------------------------------------------------------------------------------------------------- 
# --------------------------------------------- MUTUAL ---------------------------------------------- 
# ---------------------------------------------------------------------------------------------------

def use_item(item_name: str):

    if item_name.lower() not in inventory:
        print(f"Esinettä {item_name} ei löytynyt inventorysta")
        return ""

    item = inventory[item_name.lower()]

    if item["quantity"] <= 0:
        return f"{item_name.lower()} on loppu."

    if "heal" in item:
        player.health += item["heal"]
        item["quantity"] -= 1

        time.sleep(1)
        typewriter(f"Käytit {item_name} ja palautit {item['heal']}❤️, sinulla on nyt {player.health}❤️.\n")

    if game_state["state"] == "COMBAT":
        current_enemy = battle_state["enemies"][0]
        typewriter(f"⚔️ {current_enemy.name} hyökkää!", 0.03)
        enemy_attack_player()
        print(f"{player.name} health: {player.health}❤️")
        print(f"{current_enemy.name} health: {current_enemy.health}❤️")
    return ''

use_item_function = {
  "name": "use_item",
  "description": "Use an item from inventory",
  "parameters": {
    "type": "object",
    "properties": {
      "item_name": {
        "type": "string",
        "description": "Item name, e.g. health potion"
      }
    },
    "required": ["item_name"]
  }
}


def get_inventory():
    print(f"\nInventory                      {player.name}: {player.health}❤️")
    print("---------------------------------------------")
    for name, stats in inventory.items():
        print(f"{name}: {stats}")
    print("---------------------------------------------\n")
    return ""

inventory_function = {
    "name": "get_inventory",
    "description": "Get all the items in inventory"
}

# ------------------- INITIALIZING AVAILABLE FUNCTIONS -------------------

# EXPLORATION

exploration_functions = {
    "start_combat": start_combat,
    "get_inventory": get_inventory,
    "start_dialogue": start_dialogue_tool,
    "use_item": use_item,
}

exploration_tool_declarations = [
    use_item_function,
    start_combat_function,
    inventory_function,
    start_dialogue_function
]

# COMBAT

combat_functions = {
    "attack_enemy": attack_enemy,
    "use_item": use_item,
    "flee_combat": flee_combat,
    "get_inventory": get_inventory,
}

combat_tool_declarations = [
    use_item_function,
    attack_function,
    flee_combat_function,
    inventory_function,
]

