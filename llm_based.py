"""
This file I will use an LLM model to also do tokenization + sentiment analysis.
"""
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

input_text = "This is a great product. Would highly recommend! Size fits perfectly and came right on time"

prompt_instruction = """
You have two tasks:
1. Tokenize the content and return the tokens in a list.
2. Perform sentiment analysis and classify as positive, negative, or neutral.

Return the results in JSON format with keys 'tokens' and 'sentiment'.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=prompt_instruction 
    ),
    contents=input_text
)

print(response.text)
