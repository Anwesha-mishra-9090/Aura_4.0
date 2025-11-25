import os
import sys
import subprocess


def check_dependencies():
    """Check and install required dependencies"""
    required = [
        'speechrecognition',
        'pyttsx3',
        'nltk',
        'openai',
        'flask'
    ]

    print("🔍 Checking dependencies...")

    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} missing")
            install = input(f"Install {package}? (y/n): ")
            if install.lower() == 'y':
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("✅ All dependencies checked!")


def setup_nltk_data():
    """Download required NLTK data"""
    import nltk
    print("📥 Downloading NLTK data...")

    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
    except:
        print("⚠️  NLTK download failed - some features may not work")


def create_directories():
    """Create required directories"""
    directories = ['web/templates', 'web/static', 'exports', 'backups']

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")


def main():
    print("🚀 AURA v4.0 Deployment Setup")
    print("=" * 40)

    check_dependencies()
    setup_nltk_data()
    create_directories()

    print("\n🎉 Setup completed! You can now run:")
    print("  python main.py      - Text/Voice mode")
    print("  python aura_gui.py  - Graphical interface")
    print("  python web/app.py   - Web dashboard")
    print("\n💡 For AI features, set your OpenAI API key in the GUI settings")


if __name__ == "__main__":
    main()