from ai.ai_interface import ask_ai
import time
from tools import typewriter

def start_dialogue(player, npc_name, npc_role_description):
    """
    Käynnistää dialogin pelaajan ja NPC:n välille.
    
    Params:
        player       = Player olio
        npc_name     = esim. "Goblin"
        npc_role_description = lyhyt kuvaus AI:lle esim: "You are a scared goblin bullying a traveler."
    """

    # Dialogi historia:
    # Tallennetaan listaan (speaker, message)
    dialogue_history = []

    # 1) Pelaaja antaa aloitusviestin
    opening = input(f"{player.name}: ")
    dialogue_history.append((f"{player.name}", opening))

    # Ensimmäinen vastaus AI:lta
    npc_reply = generate_npc_reply(npc_name, npc_role_description, dialogue_history)
    print(f"\n{npc_name}:", end=" ")
    time.sleep(0.5)
    typewriter(npc_reply, delay=0.03)
    dialogue_history.append((npc_name, npc_reply))

    # 2) Loop kunnes AI lopettaa dialogin
    while True:
        player_msg = input(f"\n{player.name}: ")

        # pelaaja voi päättää keskustelun manuaalisesti
        if player_msg.lower() in ["lopeta", "poistu", "exit"]:
            print("Lopetit keskustelun.")
            break

        dialogue_history.append((f"{player.name}", player_msg))

        npc_reply = generate_npc_reply(npc_name, npc_role_description, dialogue_history)
        print(f"\n{npc_name}:", end=" ")
        time.sleep(0.5)
        typewriter(npc_reply, delay=0.03)
        dialogue_history.append((npc_name, npc_reply))

        # AI voi ilmoittaa että dialogi päättyy
        if any(phrase in npc_reply.lower() for phrase in [
            "en aio puhua enempää",
            "keskustelu on ohi",
            "poistu luotani",
            "ei ole enää mitään sanottavaa",
            "hyvästi"
        ]):
            print("\nKeskustelu päättyi luonnollisesti.")
            break

    return dialogue_history



def generate_npc_reply(npc_name, npc_role_description, history):
    """
    Palauttaa AI:n vastauksen perustuen dialogihistoriaan.
    """

    # Muodostetaan prompt historia
    messages = []
    for speaker, msg in history:
        if speaker == "player":
            messages.append(f"PLAYER: {msg}")
        else:
            messages.append(f"{speaker.upper()}: {msg}")

    conversation_block = "\n".join(messages)

    prompt = f"""
You are roleplaying as {npc_name}. 
{npc_role_description}

Rules:
- Always stay in character.
- Respond only as {npc_name}, never as the narrator or system.
- Keep responses short (1–3 sentences), unless more is explicitly needed.
- Do not invent player actions.
- Use the conversation history to decide tone, mood and reactions.

Conversation so far:
{conversation_block}

Now respond to the last player message.
"""

    return ask_ai(prompt).strip()
