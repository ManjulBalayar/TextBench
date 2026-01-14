"""
This file I will use an LLM model to also do tokenization + sentiment analysis.
"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import re

# Try to load API key from Streamlit secrets first (for deployment)
# Fall back to .env for local development
try:
    import streamlit as st
    if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
        os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
except ImportError:
    pass  # Streamlit not available, will use .env

load_dotenv()

client = genai.Client()

def llm_tokenizer(input_text):
    prompt_instruction = """
    Tokenize the input text into individual words (lowercase, no punctuation).

    Return ONLY valid JSON in this exact format with no extra text:
    {"tokens": ["word1", "word2", "word3"]}

    Now tokenize this text:
    """
    
    try:
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
    except Exception as e:
        # Return error info that can be displayed in the UI
        error_msg = str(e)
        if "429" in error_msg or "rate limit" in error_msg.lower():
            return {"error": "Rate limit exceeded. Please try again later."}
        elif "quota" in error_msg.lower():
            return {"error": "API quota exceeded. Please check your Gemini API usage."}
        elif "auth" in error_msg.lower() or "api key" in error_msg.lower():
            return {"error": "Authentication error. Please check your API key."}
        else:
            return {"error": f"LLM tokenization failed: {error_msg}"}

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

    try:
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
    except Exception as e:
        # Return error info that can be displayed in the UI
        error_msg = str(e)
        if "429" in error_msg or "rate limit" in error_msg.lower():
            return {
                "sentiment": "error",
                "confidence": 0,
                "reasoning": "Rate limit exceeded. Please try again later or check your API quota."
            }
        elif "quota" in error_msg.lower():
            return {
                "sentiment": "error",
                "confidence": 0,
                "reasoning": "API quota exceeded. Your free trial may have ended. Please check your Gemini API usage."
            }
        elif "auth" in error_msg.lower() or "api key" in error_msg.lower():
            return {
                "sentiment": "error",
                "confidence": 0,
                "reasoning": "Authentication error. Please check your API key configuration."
            }
        else:
            return {
                "sentiment": "error",
                "confidence": 0,
                "reasoning": f"LLM analysis failed: {error_msg}"
            }

