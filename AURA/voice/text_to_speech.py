import pyttsx3

# Initialize the TTS engine once
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
        # Adjust voice properties
        engine.setProperty('rate', 150)  # Speed percent
        engine.setProperty('volume', 0.8)  # Volume 0-1
    return engine

def speak(text):
    print(f"AURA: {text}")
    try:
        engine = get_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")