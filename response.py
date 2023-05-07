import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    response_message = completion.choices[0].message.content.strip()
    return response_message



