from ai.ai_interface import ask_ai
from tools import typewriter
from game_data import enemy_descriptions
from states import world_state, exploration_memory

def intro_scene(player):

    world_state["location"] = "Metsätie kylän ulkopuolella"
    world_state["situation"] = "Syvällä metsässä asuu iso ilkeä Orc, joka on vaaraksi tiellä kulkijoille"
    world_state["visible_entities"] = ["goblin", "kauppias", "Orc"]

    desc = enemy_descriptions.get("goblin", {})
    personality = desc.get("personality", "")

    intro_prompt =  f"""Sinä olet pelin tarinankertoja. Pelaajan nimi: {player.name}
Kuvaile lyhyesti tilanne:
Pelaaja kävelee tiellä ja näkee goblinin kiusaavan kauppiasta. 
Goblinin luonne: {personality}
Pelaajan täytyy tehdä valinta, mitä tehdä seuraavaksi. Älä kuitenkaan anna valinta vaihtoehtoja, kysy vain yksinkertaisesti, mitä pelaaja tekee?
"""
    intro_text = ask_ai(intro_prompt)
    
    typewriter(intro_text)

    exploration_memory.append({
        "player": None,
        "narration": intro_text
    })
