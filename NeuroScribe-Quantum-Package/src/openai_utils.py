"""
openai_utils.py - Handles GPT-based rewriting and prompt generation.
"""

import os
from typing import Optional
import openai
from dotenv import load_dotenv

load_dotenv()

def set_openai_api_key() -> None:
    """
    Set the OpenAI API key from environment variables.
    
    Raises:
        ValueError: If OpenAI API key is not found in environment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")
    openai.api_key = api_key

def get_gpt_response(prompt: str) -> str:
    """
    Get a response from GPT-3.5-turbo model.
    
    Args:
        prompt (str): The prompt to send to GPT.
        
    Returns:
        str: The response from GPT.
        
    Raises:
        Exception: If the API call fails.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

def rewrite_with_gpt(text: str) -> str:
    """
    Rewrite a given text using GPT-3.5-turbo.
    
    Args:
        text (str): Original input text to be rewritten.
        
    Returns:
        str: Rewritten text from GPT, or error message if processing fails.
    """
    try:
        set_openai_api_key()
        prompt = f"""
        Please rewrite the following text to improve clarity, grammar, and flow:
        
        {text}
        
        Return only the rewritten text without any additional commentary.
        """
        return get_gpt_response(prompt)
    except Exception as e:
        return f"Error processing with GPT: {str(e)}" 