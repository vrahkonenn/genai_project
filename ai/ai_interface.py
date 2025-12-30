from google import genai
from google.genai import types

client = genai.Client()

def ask_ai(prompt: str, tools=False, model: str = "gemini-2.5-flash-lite"):

    if tools == True:
        tools = types.Tool(function_declarations=tool_declarations)
        config = types.GenerateContentConfig(tools=[tools])

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
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
            print(response.text)

    else:
        """
        Lähettää promptin AI:lle ja palauttaa AI:n vastauksen tekstinä.
    
        """
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text.strip()