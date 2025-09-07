# JARVIS-AI 🤖

Welcome to JARVIS-AI, a personal assistant project inspired by Iron Man’s JARVIS. This is Seif’s first full-stack AI assistant, built from scratch with voice control, smart responses, and modular design.

## ✅ Version 1.0 Highlights

- 🎧 Voice command recognition
- 🔊 Text-to-speech responses
- 🧠 AI replies using Gemini 2.5 Pro via OpenRouter
- 🗺️ App launching (Notepad, Calculator, Chrome, etc.)
- 🌐 Web search and site shortcuts (Google, YouTube, Wikipedia)
- 🔐 Secure API key using `.env`
- 📚 Documentation folder with config and module breakdown
- 🧹 Clean repo using `.gitignore`
- 🗂️ Modular folder structure for future expansion

## 🗂️ Project Structure

See below for how the project is organized:
JARVIS-AI/
│
├── jarvis.py               # Main assistant script
├── .env                    # API key (not pushed to GitHub)
├── .gitignore              # Keeps sensitive files out of repo
│
├── voice/                  # Voice input/output modules
│   └── __init__.py
│
├── ai/                     # AI response logic
│   └── __init__.py
│
├── utils/                  # Helper functions (web actions, etc.)
│   └── __init__.py
│
├── docs/                   # Project documentation
│   ├── overview.md
│   └── config.md
│
└── README.md               # Project intro and guide


## 🚀 What’s Next (Version 2.0 Roadmap)

- Add GUI interface
- Expand command library
- Connect to smart home devices
- Add logging and error tracking
- Create a setup script for easy installation

## 👨‍💻 Author

**Seif** — aspiring developer building his first AI assistant.
