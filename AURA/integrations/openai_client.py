import openai
import os
from utils.config_manager import get_config

# Initialize OpenAI client
client = None

def initialize_ai():
    """Initialize OpenAI client with API key"""
    global client
    config = get_config()

    api_key = config.get('openai_api_key')
    if not api_key:
        # SILENT MODE - No warning messages
        return False

    try:
        client = openai.OpenAI(api_key=api_key)
        # Test the connection with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'AI connected' in a creative way."}],
            max_tokens=20
        )
        print("🤖 " + response.choices[0].message.content)
        return True
    except Exception as e:
        # SILENT MODE - No error messages
        return False

def chat_with_gpt(message, context=""):
    """Chat with OpenAI GPT"""
    if not client:
        return "I'd be happy to help with that! How can I assist you?"

    try:
        messages = []
        if context:
            messages.append({"role": "system", "content": context})

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"I'd be happy to help with that! How can I assist you?"

def summarize_text(text):
    """Summarize text using AI"""
    if not client:
        return "I can help you summarize that! What would you like me to focus on?"

    prompt = f"Please summarize the following text concisely:\n\n{text}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return "I can help you summarize that! What would you like me to focus on?"

def generate_content(topic, content_type="paragraph"):
    """Generate content using AI"""
    if not client:
        return f"I can help you create content about {topic}! What specific aspect would you like me to focus on?"

    prompts = {
        "paragraph": f"Write a paragraph about: {topic}",
        "email": f"Write a professional email about: {topic}",
        "ideas": f"Generate creative ideas about: {topic}",
        "plan": f"Create a step-by-step plan for: {topic}"
    }

    prompt = prompts.get(content_type, f"Write about: {topic}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I can help you create content about {topic}! What specific aspect would you like me to focus on?"

def analyze_sentiment(text):
    """Analyze sentiment of text"""
    if not client:
        return "neutral"

    prompt = f"Analyze the sentiment of this text and respond with only one word: positive, negative, or neutral:\n\n{text}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.1
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        return "neutral"