import random
from integrations.openai_client import chat_with_gpt, summarize_text, generate_content


def chat_with_ai(message):
    """Enhanced AI chat with real GPT integration"""

    # Use real AI if available, otherwise fallback to basic responses
    try:
        # Add context about AURA for better responses
        context = "You are AURA, a helpful AI personal assistant focused on productivity, task management, and personal development. Be concise, helpful, and encouraging."

        response = chat_with_gpt(message, context)
        if response and not response.startswith("AI error"):
            return response
    except:
        pass  # Fall back to basic responses

    # Fallback basic responses
    message_lower = message.lower()

    if any(word in message_lower for word in ['learn', 'study', 'education']):
        responses = [
            "Learning is a journey! What specific topic interests you?",
            "Continuous learning is key to growth. I can help you create a study plan!",
            "That's great! Breaking learning into daily habits works best."
        ]
    elif any(word in message_lower for word in ['productive', 'efficient', 'work']):
        responses = [
            "Try time-blocking: schedule specific times for different types of work.",
            "The Pomodoro technique (25min work, 5min break) boosts focus significantly.",
            "Prioritize tasks using the Eisenhower Matrix - focus on what's important!"
        ]
    else:
        responses = [
            f"I understand you're asking about '{message}'. How can I help you take action on this?",
            f"That's interesting! Regarding '{message}', what's the most important aspect for you?",
            f"Great question! Have you considered breaking '{message}' into smaller steps?",
            f"I'd love to help with '{message}'. What would you like to achieve?"
        ]

    return random.choice(responses)


def ai_summarize(text):
    """Use AI to summarize text"""
    return summarize_text(text)


def ai_write(topic, content_type="paragraph"):
    """Use AI to generate content"""
    return generate_content(topic, content_type)


def get_ai_insights():
    """Generate AI-powered productivity insights"""
    try:
        prompt = "Give one concise, encouraging productivity insight or tip (max 2 sentences)"
        insight = chat_with_gpt(prompt, "You are a productivity coach")
        if insight and not insight.startswith("AI error"):
            return f"💡 {insight}"
    except:
        pass

    # Fallback insights
    insights = [
        "📊 Consistency beats intensity when building habits. Small daily actions create big results!",
        "🎯 Focus on completing one important task first thing in the morning.",
        "⏰ Regular breaks improve focus. Try the 52-17 rule: 52 minutes work, 17 minutes break.",
        "🌟 Celebrate small wins - they build momentum and motivation!"
    ]
    return random.choice(insights)