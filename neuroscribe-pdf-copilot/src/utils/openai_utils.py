import os
import openai
from dotenv import load_dotenv

load_dotenv()

def set_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")
    openai.api_key = api_key

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

def rewrite_with_gpt(command, text_blocks):
    """Rewrite text blocks using GPT based on the given command"""
    set_openai_api_key()
    
    # Combine all text blocks into a single text
    full_text = "\n".join([block.get('text', '') for block in text_blocks])
    
    # Create the prompt
    prompt = f"""
    Command: {command}
    
    Text to process:
    {full_text}
    
    Please process the text according to the command. Return the processed text.
    """
    
    try:
        response = get_gpt_response(prompt)
        return response
    except Exception as e:
        return f"Error processing with GPT: {str(e)}"