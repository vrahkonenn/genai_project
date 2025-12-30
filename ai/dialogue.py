from states import dialogue_state
from ai.ai_interface import ask_ai
from tools import typewriter
import time

# Avainsanoja joilla päättää keskustelu
exit_keywords = [
    "lopeta",
    "lopeta keskustelu",
    "poistu",
    "lähde",
    "kävele pois",
    "hyvästi",
    "en halua jatkaa",
    "lopetan keskustelun",
    "hei hei",

    "exit",
    "quit",
    "leave",
    "walk away",
    "goodbye",
    "bye",
    "end conversation",
    "stop talking",
]

def generate_npc_reply(npc_name, npc_role_description, history):
    """
    Palauttaa AI:n vastauksen perustuen dialogihistoriaan.
    """

    # Muodostetaan prompt historia
    messages = []
    for speaker, msg in history:
        if speaker == "PLAYER":
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

        
def send_player_msg(player_msg):
    dialogue_state["history"].append(("PLAYER", player_msg))
    npc_name = dialogue_state["npc_name"]
    npc_role_description = dialogue_state["npc_personality"]
    dialogue_history = dialogue_state["history"]
    npc_reply = generate_npc_reply(npc_name, npc_role_description, dialogue_history)
    print(f"\n{npc_name}:", end=" ")
    time.sleep(0.5)
    typewriter(npc_reply, delay=0.03)
    dialogue_history.append((npc_name, npc_reply))
