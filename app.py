from google import genai
from google.genai import types
from states import game_state, dialogue_state, world_state, exploration_memory 
from tools import exploration_functions, exploration_tool_declarations, combat_functions, combat_tool_declarations, typewriter
from game_data import player_start_stats
from ai.dialogue import send_player_msg, exit_keywords
from scenes.intro import intro_scene
from entities.player import Player
from ai.game_master_prompt import GAME_MASTER_PROMPT

print("\n\n\nTervetuloa tekstiseikkailu peliin.\nSyötä hahmollesi haluamasi nimi ja ala pelaamaan! (tyhjä syöttö = oletusnimi)")
player_name= input('> ')
if player_name:
    player_start_stats["name"] = player_name
player = Player(**player_start_stats, inventory={})

intro_scene(player) 

while True:
    if game_state["state"] != "DIALOGUE":
        player_input = input('\n> ')

    if game_state["state"] == "EXPLORATION":
        available_functions = exploration_functions
        tool_declarations = exploration_tool_declarations

        memory_block = ""
        for entry in exploration_memory[-3:]:
            memory_block += f"PLAYER: {entry['player']}\n"
            memory_block += f"NARRATOR: {entry['narration']}\n"

        world_block = f"""
        CURRENT WORLD STATE:
        Location: {world_state['location']}
        Situation: {world_state['situation']}
        Visible entities: {", ".join(world_state['visible_entities'])}
        """

        full_prompt = f"""
        {GAME_MASTER_PROMPT}

        {world_block}

        RECENT EVENTS:
        {memory_block}

        PLAYER ACTION:
        {player_input}
        """

    elif game_state["state"] == "COMBAT":
        available_functions = combat_functions
        tool_declarations = combat_tool_declarations
        full_prompt = player_input

    if game_state["state"] == "DIALOGUE":
        while True:
            player_msg = input(f"{player_start_stats["name"]}: ")
            if player_msg.lower() in exit_keywords:
                typewriter(f"❌💬 Lopetetaan keskustelu henkilön {dialogue_state["npc_name"]} kanssa... ❌🗣️")
                game_state["state"] = "EXPLORATION"
                break
            send_player_msg(player_msg)
        continue


    print('')

    client = genai.Client()
    tools = types.Tool(function_declarations=tool_declarations)
    config = types.GenerateContentConfig(tools=[tools])

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=full_prompt,
        config=config
    )

    part = response.candidates[0].content.parts[0]

    # Check if AI wants to call a function
    if part.function_call:
        function_call = part.function_call
        fn = available_functions.get(function_call.name)
        if fn:
            result = fn(**function_call.args)
            print(result)
        else:
            print("Function not found!")
    else:
        typewriter(response.text)
        exploration_memory.append({
            "player": player_input,
            "narration": response.text
        })

        if len(exploration_memory) > 10:
            exploration_memory.pop(0)
