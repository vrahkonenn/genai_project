from game_data import inventory, enemy_templates, player_start_stats, enemy_descriptions
from entities.player import Player
from entities.enemy import Enemy
import time
from google import genai
from states import battle_state
from ai.generate_battle_texts import generate_battle_text, generate_enemy_battle_text

player = Player(
    **player_start_stats,
    inventory = inventory
)

current_enemy = Enemy(
    "Goblini", **enemy_templates["goblin"]
)

GAME_WORLD = {
    "npcs": {}
}

def typewriter(text: str, delay: float = 0.04):
    """Tulostaa tekstin kirjain kerrallaan näyttävästi."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # Rivinvaihto lopuksi
    time.sleep(1)

# ------------------- CREATING NPC -------------------

def create_npc(name: str, role: str, description: str, location: str):
    """
    Creates an NPC object and stores it in the global GAME_WORLD.
    This is called via AI tool invocation.
    """

    npc = {
        "name": name,
        "role": role,
        "description": description,
        "location": location,
        "dialogue_history": []
    }

    GAME_WORLD["npcs"][name] = npc

    return {
        "status": "npc_created",
        "npc": npc
}

create_npc_function = {
    "name": "create_npc",
    "description": "Create a new NPC and add it to the game world. Use this whenever the player meets a new character.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "NPC name"},
            "role": {"type": "string", "description": "NPC's social role or job"},
            "description": {"type": "string", "description": "Short description of personality and appearance"},
            "location": {"type": "string", "description": "Where the NPC currently is"}
        },
        "required": ["name", "role", "description", "location"]
    }
}

# ------------------- ATTACKING -------------------

def attack_enemy(weapon: str):
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
        time.sleep(1)
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
        battle_state=battle_state
    )

    battle_state["history"].append(ai_text)

    typewriter("\n" + ai_text + "\n")

    return ""

# ------------------- OPENING INVENTORY -------------------
def get_inventory():
    print("\nInventory:")
    print("---------------------------------------------")
    for name, stats in inventory.items():
        print(f"{name}: {stats}")
    print("---------------------------------------------\n")
    return ""

inventory_function = {
    "name": "get_inventory",
    "description": "Get all the items in inventory"
}


# ------------------- GETTING SPECIFIC ITEM -------------------
def get_specific_item(item: str) -> str:
    return inventory.get(item, "You don't have that item in inventory")

specific_item_function = {
    "name": "get_specific_item",
    "description": "Gets the stats of a given weapon.",
    "parameters": {
        "type": "object",
        "properties": {
            "item": {
                "type": "string",
                "description": "The item name, e.g. axe"
            }
        },
        "required": ["item"]
    }
}


# ------------------- INITIALIZING AVAILABLE FUNCTIONS -------------------
available_functions = {
    "attack_enemy": attack_enemy,
    "get_inventory": get_inventory,
    "get_specific_item": get_specific_item,
    "create_npc": create_npc,
}

tool_declarations = [
    specific_item_function,
    inventory_function,
    attack_function,
    create_npc_function
]
