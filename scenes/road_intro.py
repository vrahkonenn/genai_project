from ai.ai_interface import ask_ai
from tools import typewriter
from game_data import enemy_descriptions
from ai.dialogue import start_dialogue

def road_intro_scene(player):

    desc = enemy_descriptions.get("goblin", {})
    personality = desc.get("personality", "")

    intro_prompt =  f"""Sinä olet pelin tarinankertoja. Pelaajan nimi: {player.name}
Kuvaile lyhyesti tilanne:
Pelaaja kävelee tiellä ja näkee goblinin kiusaavan ohikulkijaa. 
Goblinin luonne: {personality}
Pelaajan täytyy tehdä valinta, mitä tehdä seuraavaksi. Älä kuitenkaan anna valinta vaihtoehtoja, kysy vain yksinkertaisesti, mitä pelaaja tekee?
"""
    intro_text = ask_ai(intro_prompt)
    
    typewriter(intro_text, delay=0.03)

    player_input = input("> ")

    choice_prompt = f"""
Pelaaja näkee pienen goblinin kiusaavan ohikulkijaa. Pelaaja voi tehdä yhden seuraavista:
1) Hyökkää goblinin kimppuun ja taistele.
2) Yritä puhua goblinille ja neuvotella.
3) Jätä tilanne väliin ja kävele ohi.

Pelaaja kirjoittaa vapaasti, mitä hän haluaa tehdä. Analysoi pelaajan syöte ja palauta selkeäksi valinnaksi yksi seuraavista: "fight", "talk", "ignore".

Pelaajan syöte: {player_input}
"""
    
    choice = ask_ai(choice_prompt)


    if choice == "fight":
        print("💥 Pelaaja hyökkää goblinin kimppuun!")
    elif choice == "talk":
        typewriter("\nAloitat keskustelun goblinin kanssa...\n")
        start_dialogue(player, "Goblin", personality)

    elif choice == "ignore":
        print("🚶 Pelaaja kävelee ohi tapahtumasta.")



    return 0
