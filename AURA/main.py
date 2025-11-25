import os
import sqlite3
import re
import speech_recognition as sr
from memory.database import setup_database
from voice.speech_to_text import listen, text_input
from voice.text_to_speech import speak
from voice.wake_word import start_wake_word_detection
from brain.nlp_processor import process_command
from memory.memory_manager import save_conversation
from memory.reminder_manager import check_reminders, get_daily_summary
from brain.habit_tracker import get_habit_summary
from brain.smart_suggestions import get_smart_suggestions
from utils.data_export import export_data
from utils.config_manager import get_config, save_config
from integrations.openai_client import initialize_ai


def detect_wake_word(text):
    """
    Improved wake word detection with fuzzy matching
    """
    if not text:
        return False

    text_lower = text.lower().strip()

    # Exact matches
    exact_matches = ["hey aura", "hello aura", "hi aura", "aura"]

    # Fuzzy matches using regex patterns
    patterns = [
        r'hey\s*aura',
        r'hi\s*aura',
        r'hello\s*aura',
        r'hai\s*aura',
        r'hai\s*hora',
        r'hey\s*hora',
        r'^aura\s+',
        r'^aura$'
    ]

    # Check exact matches first
    if any(wake_word in text_lower for wake_word in exact_matches):
        return True

    # Check pattern matches
    for pattern in patterns:
        if re.search(pattern, text_lower):
            return True

    # Additional check for partial matches
    words = text_lower.split()
    if any(word in ["aura", "ora", "hora"] for word in words):
        if any(word in ["hey", "hi", "hello", "hai"] for word in words):
            return True

    return False


def listen_for_wake_word():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 300  # Adjust sensitivity
        recognizer.pause_threshold = 0.8  # Shorter pauses

        print("🔊 Listening for wake word...")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            text = recognizer.recognize_google(audio).lower()

            print(f"Detected: {text}")

            # Use improved wake word detection
            if detect_wake_word(text):
                print("✅ Wake word detected! Listening for command...")
                return True

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")

    return False


def listen_for_command():
    """
    Listen for actual command after wake word
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("🎤 Listening for command...")

    with microphone as source:
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"📝 Command: {command}")
            return command
        except sr.WaitTimeoutError:
            print("⏰ No command detected")
        except sr.UnknownValueError:
            print("❓ Could not understand command")

    return None


def improved_wake_word_detection():
    """Improved wake word detection with better voice recognition"""
    print("🔊 Wake word detector active...")

    while True:
        try:
            if listen_for_wake_word():
                # Wake word detected, now listen for command
                command = listen_for_command()

                if command and "stop listening" in command.lower():
                    print("🛑 Stopping voice assistant...")
                    speak("Stopping voice assistant")
                    break
                elif command:
                    # Process the command
                    response = process_command(command)
                    print(f"AURA: {response}")
                    speak(response)
                    save_conversation(command, response)
                else:
                    print("❓ No command detected after wake word")

        except KeyboardInterrupt:
            print("\n🛑 Voice assistant stopped by user")
            break
        except Exception as e:
            print(f"Voice assistant error: {e}")
            continue


def fix_database():
    """Fix corrupted database by creating a new one"""
    print("🔧 Checking database...")

    db_file = 'aura.db'
    backup_file = 'aura.db.backup'

    # Check if database exists and is healthy
    if os.path.exists(db_file):
        try:
            # Test if database is readable
            conn = sqlite3.connect(db_file)
            conn.execute("SELECT 1")
            conn.close()
            print("✅ Database is healthy")
            return True
        except sqlite3.DatabaseError:
            print("⚠️  Database corrupted, attempting to fix...")
            # Don't try to fix here - let the force fix script handle it
            return False
        except Exception as e:
            print(f"⚠️  Database error: {e}")
            return False
    else:
        print("📁 No database found - will create new one")
        return True  # No database exists, so we can create one


# Helper functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    banner = """
    ╔══════════════════════════════════════╗
    ║               A U R A                ║
    ║      AI Personal Assistant v4.0      ║
    ╚══════════════════════════════════════╝
    """
    print(banner)


def initialize_aura():
    print("🚀 Initializing AURA v4.0...")

    # Check database first
    db_ok = fix_database()

    if not db_ok:
        print("\n❌ DATABASE IS CORRUPTED!")
        print("💡 Please run: python force_fix_database.py")
        print("   Then run AURA again.")
        return False

    # Load configuration
    config = get_config()
    print("📁 Configuration loaded")

    # Setup database
    print("📊 Setting up database...")
    try:
        setup_database()
        print("✅ Database setup completed")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

    # Initialize AI
    print("🧠 Initializing AI engine...")
    ai_ready = initialize_ai()
    if ai_ready:
        print("✅ AI engine ready")
    else:
        print("⚠️  AI engine offline - using basic mode")

    # Check for reminders
    try:
        reminders = check_reminders()
        if reminders:
            print("\n🔔 Reminders:")
            for reminder in reminders:
                print(f"  {reminder}")
    except Exception as e:
        print(f"⚠️  Could not check reminders: {e}")

    # Show daily summary
    try:
        summary = get_daily_summary()
        if summary:
            print(f"\n{summary}")
    except Exception as e:
        print(f"⚠️  Could not get daily summary: {e}")

    # Show habit summary
    try:
        habit_summary = get_habit_summary()
        if habit_summary:
            print(f"\n{habit_summary}")
    except Exception as e:
        print(f"💪 Habit tracking ready to use")

    # Show smart suggestions
    try:
        suggestions = get_smart_suggestions()
        if suggestions:
            print(f"\n💡 Smart Suggestions:\n{suggestions}")
    except Exception as e:
        print(f"💡 Keep using AURA for personalized suggestions!")

    print("\n🎯 Available Modes:")
    print("1. Text Mode")
    print("2. Voice Mode")
    print("3. Voice Assistant (Always Listening)")
    print("4. GUI Mode")
    print("5. Web Dashboard")

    print("\n✅ AURA v4.0 is ready!")
    speak("AURA version 4 point 0 initialized and ready!")
    return True


def show_help():
    help_text = """
📋 AURA v4.0 - AVAILABLE COMMANDS:

🤖 AI FEATURES:
• "chat [message]" - Talk with AI
• "ai summarize [text]" - AI text summarization
• "ai write [topic]" - AI content generation
• "suggest tasks" - AI task suggestions

📅 TASKS & HABITS:
• "add task [description]" - Add task
• "add task [description] tomorrow high priority" - Advanced task
• "show tasks" - List tasks
• "complete task 1" - Complete task
• "add habit [name] daily" - Track habit
• "mark habit [name] done" - Complete habit

🎵 VOICE CONTROL:
• "Hey Aura" - Wake word (in voice assistant mode)
• "stop listening" - Stop voice mode
• "mute/unmute" - Toggle voice

📊 ANALYTICS:
• "productivity report" - Detailed analytics
• "habit stats" - Habit analytics
• "task stats" - Task statistics
• "export data" - Export all data

🔧 SYSTEM:
• "help" - Show this help
• "settings" - Configure AURA
• "switch to gui" - Open graphical interface
• "quit" - Exit AURA

Examples:
• "chat what's the weather today?"
• "ai write a poem about coding"
• "add task finish project by friday high priority"
• "productivity report"
"""
    print(help_text)


def voice_assistant_mode():
    """Always-listening voice assistant mode with improved wake word detection"""
    print("\n🎤 Voice Assistant Mode Activated!")
    print("Say 'Hey Aura' to wake me up, or 'stop listening' to exit")
    speak("Voice assistant mode activated. Say Hey Aura to wake me up.")

    try:
        # Use the improved wake word detection
        improved_wake_word_detection()
    except Exception as e:
        print(f"Voice assistant error: {e}")
        print("Switching to manual voice mode...")
        manual_voice_mode()


def manual_voice_mode():
    """Manual voice mode (push-to-talk)"""
    print("\n🎤 Manual Voice Mode - Press Enter to start listening")

    while True:
        try:
            input("Press Enter to speak...")
            user_input = listen()

            if user_input is None:
                continue

            if user_input.lower() in ['quit', 'exit', 'stop listening']:
                break

            response = process_command(user_input)
            speak(response)
            save_conversation(user_input, response)
        except KeyboardInterrupt:
            print("\n👋 Exiting voice mode...")
            break
        except Exception as e:
            print(f"Voice mode error: {e}")


def text_mode():
    """Traditional text mode"""
    print("\n⌨️ Text Mode - Type your commands")
    print("Type 'help' for commands, 'quit' to exit")

    while True:
        try:
            user_input = text_input()
            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.lower() == 'switch to gui':
                start_gui_mode()
                break
            elif user_input.lower() == 'help':
                show_help()
                continue

            response = process_command(user_input)
            print(f"\nAURA: {response}")
            save_conversation(user_input, response)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def start_gui_mode():
    """Launch graphical interface"""
    try:
        from aura_gui import start_gui
        print("🖥️  Starting GUI mode...")
        start_gui()
    except ImportError as e:
        print(f"GUI mode not available: {e}")
        print("Falling back to text mode...")
        text_mode()
    except Exception as e:
        print(f"GUI error: {e}")
        print("Falling back to text mode...")
        text_mode()


def start_web_dashboard():
    """Launch web dashboard"""
    try:
        from web.app import start_web_server
        print("\n🌐 Starting web dashboard on http://localhost:5000")
        start_web_server()
    except ImportError as e:
        print(f"Web dashboard not available: {e}")
        print("Falling back to text mode...")
        text_mode()
    except Exception as e:
        print(f"Web dashboard error: {e}")
        print("Falling back to text mode...")
        text_mode()


def main():
    clear_screen()
    print_banner()

    if not initialize_aura():
        print("❌ AURA failed to initialize. Please check the errors above.")
        return

    # Choose mode
    print("\n" + "=" * 50)

    while True:
        try:
            mode = input("Choose mode (1-5): ").strip()

            if mode == "1":
                text_mode()
                break
            elif mode == "2":
                manual_voice_mode()
                break
            elif mode == "3":
                voice_assistant_mode()
                break
            elif mode == "4":
                start_gui_mode()
                break
            elif mode == "5":
                start_web_dashboard()
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Starting text mode as fallback...")
            text_mode()
            break


if __name__ == "__main__":
    main()