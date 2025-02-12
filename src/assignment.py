import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor
import os

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

def run(user_input):
    client = Groq(
        api_key=os.environ.get(
            os.environ.get("GROQ_API_KEY"),
        ),
    )

    client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        response_model=Character,
    )
    print(resp.model_dump_json(indent=2))

def get_user_input():
    return input("Enter a topic or question to learn about (or 'exit' to quit): ")

if __name__ == "__main__":
    while True:
        user_input = get_user_input()
        if user_input.lower() == 'exit':
            break
        run(user_input)

