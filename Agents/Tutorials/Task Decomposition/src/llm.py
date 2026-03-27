from .config import MODEL
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

class LLM():
    def __init__(self):
        self.model = MODEL
        self.client = Groq()
        self.max_completion_tokens = 2000
        
    def generate(self, systemPrompt, userPrompt):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": systemPrompt
                },
                {
                    "role": "user",
                    "content": userPrompt,
                }
            ],
            model=self.model,
            max_completion_tokens=self.max_completion_tokens,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
            
    
    
    
# llm = LLM()
# response = llm.generate("what kind of model are you?")
# print(response)