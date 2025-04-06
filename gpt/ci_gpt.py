import os
from dotenv import load_dotenv
import openai

load_dotenv()

class GPTKachelAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def prompt(self, user_prompt):
        messages = [
            {
                "role": "system",
                "content": (
                    "Du bist ein visueller und technischer Designassistent für politische Öffentlichkeitsarbeit – "
                    "spezialisiert auf das Corporate Design der AfD laut Handbuch (Stand Februar 2024). "
                    "Du hilfst bei der Gestaltung von Social Media Kacheln, Flyern, Bannern und sonstigen Formaten."
                )
            },
            {"role": "user", "content": user_prompt}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Fehler bei der GPT-Anfrage: {e}"
