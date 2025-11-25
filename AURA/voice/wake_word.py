import speech_recognition as sr
import threading
import time
from voice.speech_to_text import listen
from voice.text_to_speech import speak
from brain.nlp_processor import process_command
from memory.memory_manager import save_conversation


class WakeWordDetector:
    def __init__(self):
        self.listening = False
        self.wake_phrases = ["hey aura", "hello aura", "okay aura", "wake up"]

    def detect_wake_word(self, text):
        """Check if text contains wake word"""
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in self.wake_phrases)

    def listen_loop(self):
        """Main listening loop"""
        recognizer = sr.Recognizer()

        print("🔊 Wake word detector active...")

        while self.listening:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)

                text = recognizer.recognize_google(audio)
                print(f"Detected: {text}")

                if self.detect_wake_word(text):
                    print("🎯 Wake word detected!")
                    speak("Yes? How can I help you?")
                    self.handle_command_mode()

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                if self.listening:  # Only print errors if still listening
                    print(f"Wake word error: {e}")

    def handle_command_mode(self):
        """Handle commands after wake word"""
        speak("I'm listening...")

        try:
            user_input = listen()
            if user_input and user_input.lower() not in ['stop listening', 'never mind']:
                response = process_command(user_input)
                speak(response)
                save_conversation(user_input, response)
            else:
                speak("Going back to sleep.")

        except Exception as e:
            print(f"Command handling error: {e}")
            speak("Sorry, I didn't catch that.")

    def start(self):
        """Start wake word detection"""
        self.listening = True
        self.listen_loop()

    def stop(self):
        """Stop wake word detection"""
        self.listening = False


def start_wake_word_detection():
    """Start the wake word detector"""
    detector = WakeWordDetector()

    try:
        detector.start()
    except KeyboardInterrupt:
        detector.stop()
        print("\n👋 Wake word detector stopped")
    except Exception as e:
        print(f"Wake word detector error: {e}")