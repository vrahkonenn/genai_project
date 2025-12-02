from google import genai

client = genai.Client()

def ask_ai(prompt: str, model: str = "gemini-2.5-flash-lite") -> str:
    """
    Lähettää promptin AI:lle ja palauttaa AI:n vastauksen tekstinä.

    """
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text.strip()
