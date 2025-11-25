# AURA - AI Personal Assistant v4.0

Demo for the project is here - [ https://drive.google.com/drive/folders/1VP2GUPjplmEQuI9t3as44lv3QnY85Glk?usp=sharing ] 
I have uploaded my all demos in the drive you can check there 
Voice feature normally works, but in this demo I used text input due to a temporary throat infection. There is demo for voice but that is not clear but if you do this it can work fine for you . Thank you . 


<div align="center">

![AURA Banner](https://img.shields.io/badge/AURA-AI%20Assistant-v4.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Your Intelligent Personal Assistant with Voice Recognition & Task Management**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Demo](#demo) • [Contributing](#contributing)

</div>

## 🎯 Overview

AURA is an advanced AI-powered personal assistant that combines voice recognition, natural language processing, and smart task management to help you stay productive and organized.

## ✨ Features

### 🎤 Voice Intelligence
- **Advanced Voice Recognition** - Improved wake word detection ("Hey Aura")
- **Multi-mode Voice Assistant** - Always listening or push-to-talk
- **Speech-to-Text & Text-to-Speech** - Natural conversations

### 🤖 AI Capabilities
- **Smart NLP Processing** - Understands context and intent
- **Task Automation** - Automatic task categorization
- **Habit Tracking** - Daily habit monitoring and analytics
- **Smart Suggestions** - Personalized productivity insights

### 📊 Productivity Tools
- **Task Management** - Add, complete, and track tasks
- **Habit Tracker** - Build and maintain daily habits
- **Reminder System** - Never miss important deadlines
- **Productivity Analytics** - Detailed reports and insights

### 🎨 Multiple Interfaces
- **Text Mode** - Traditional command-line interface
- **Voice Mode** - Hands-free voice control
- **GUI Mode** - Graphical user interface
- **Web Dashboard** - Browser-based access

## 🛠 Installation

### Prerequisites
- Python 3.8 or higher
- Microphone (for voice features)

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/aura-ai-assistant.git
cd aura-ai-assistant
Install dependencies

bash
pip install -r requirements.txt
Run AURA

bash
python main.py
Detailed Setup
For detailed installation instructions, see INSTALLATION.md

🎮 Usage
Starting AURA
bash
python main.py
Available Modes
Text Mode - Type commands directly

Voice Mode - Push-to-talk voice commands

Voice Assistant - Always listening for "Hey Aura"

GUI Mode - Graphical interface

Web Dashboard - Browser interface

Basic Commands
bash
# AI Features
"chat what's the weather today?"
"ai write a poem about coding"

# Task Management  
"add task finish project by friday high priority"
"show tasks"
"complete task 1"

# Habit Tracking
"add habit exercise daily"
"mark habit exercise done"


Manage tasks and habits with natural language

🏗 Project Structure
text
aura-ai-assistant/
├── main.py                 # Main application entry point
├── brain/                  # AI and NLP processing
│   ├── nlp_processor.py    # Natural language processing
│   ├── habit_tracker.py    # Habit management
│   └── smart_suggestions.py # AI suggestions
├── voice/                  # Voice capabilities
│   ├── speech_to_text.py   # Voice recognition
│   ├── text_to_speech.py   # Speech synthesis
│   └── wake_word.py        # Wake word detection
├── memory/                 # Data management
│   ├── database.py         # Database operations
│   ├── memory_manager.py   # Conversation memory
│   └── reminder_manager.py # Reminder system
├── integrations/           # External services
│   └── openai_client.py    # AI integration
└── utils/                  # Utilities
    ├── config_manager.py   # Configuration
    └── data_export.py      # Data export
🔧 Configuration
Edit config/settings.json to customize AURA:

json
{
    "ai_provider": "openai",
    "voice_enabled": true,
    "wake_word": "hey aura",
    "auto_start": false
}
🤝 Contributing
We love contributions! Please see our Contributing Guide for details.

Development Setup
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request

📝 License
This project is licensed under the MIT License - see LICENSE file for details.

🙏 Acknowledgments
SpeechRecognition library for voice capabilities

OpenAI for AI integration

SQLite for lightweight database management

<div align="center">
⭐ Don't forget to star this repo if you find it helpful!

Report Bug •
Request Feature •
Follow Updates

</div> ```
2. Create Additional Documentation Files
requirements.txt

txt
speechrecognition==3.10.0
pyttsx3==2.90
pyaudio==0.2.11
sqlite3
requests==2.31.0
flask==2.3.3
python-dotenv==1.0.0
openai==0.28.0
numpy==1.24.3
LICENSE

txt
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

3. GitHub Upload Steps
bash
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "feat: Initial release of AURA AI Assistant v4.0

- Advanced voice recognition with improved wake word detection
- Multi-mode interface (text, voice, GUI, web)
- AI-powered task management and habit tracking
- Smart NLP processing and productivity analytics
- Database management and reminder system"

# Create GitHub repository first, then:
git remote add origin https://github.com/yourusername/aura-ai-assistant.git
git branch -M main
git push -u origin main
