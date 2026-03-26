from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class LLM:
    def __init__(self, model):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model

    def call(self, messages):
        res = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=5000
        )
        return res.choices[0].message.content