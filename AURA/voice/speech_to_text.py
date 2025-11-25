import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Listening... (speak now)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

        text = recognizer.recognize_google(audio)
        print(f"👤 You said: {text}")
        return text

    except sr.WaitTimeoutError:
        print("No speech detected")
        return None
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None
    except Exception as e:
        print(f"Microphone error: {e}. Please check your microphone.")
        return None


# Fallback text input
def text_input():
    return input("👤 You (type): ")