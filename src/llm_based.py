"""
This file I will use an LLM model to also do tokenization + sentiment analysis.
"""
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import re
import ast

load_dotenv()

client = genai.Client()

input_text = "This is a great product. Would highly recommend! Size fits perfectly and came right on time"

def llm_tokenizer(input_text):
    prompt_instruction = """
    Tokenize the input text into individual words (lowercase, no punctuation).

    Return ONLY valid JSON in this exact format with no extra text:
    {"tokens": ["word1", "word2", "word3"]}

    Now tokenize this text:
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompt_instruction
        ),
        contents=input_text
    )
    
    result_text = response.text.strip()
    
    # Remove markdown if present
    if result_text.startswith('```'):
        result_text = re.sub(r'```(?:json)?\s*|\s*```', '', result_text).strip()
    
    result = json.loads(result_text)
    return result["tokens"]

def llm_sentiment_analysis(input_text):
    prompt_instruction = """
    Analyze the sentiment of the given text and provide:
    1. Classification: positive, negative, or neutral
    2. Confidence score: 0-100 representing your certainty
    3. Reasoning: Brief explanation for your classification

    Return JSON format:
    {
        "sentiment": "positive|negative|neutral",
        "confidence": 85,
        "reasoning": "Contains strong positive words..."
    }
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompt_instruction 
        ),
        contents=input_text
    )

    result_text = response.text.strip()
    # Extract JSON from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
    if json_match:
        result_text = json_match.group(1)

    result = json.loads(result_text)
    return result

result = llm_tokenizer(input_text)
print(result)
