import openai
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")

def rewrite_text(prompt):
    openai.api_key = get_openai_api_key()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

def summarize_text(text):
    prompt = f"Please summarize the following text:\n\n{text}"
    return rewrite_text(prompt)