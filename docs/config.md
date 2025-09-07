# 🔐 Configuration Guide for JARVIS-AI

## 📦 What is `.env`?

The `.env` file stores sensitive information like API keys. It keeps secrets out of your code and out of GitHub.

## 🧪 Why Use It?

- Keeps your API key private
- Makes your code safer and cleaner
- Allows different users to use their own keys without editing the script

## 🛠️ How to Set It Up

1. Create a file named `.env` in the root of your project folder (`JARVIS-AI`)
2. Add your OpenRouter API key like this: OPENROUTER_KEY=your-api-key-here
3. Make sure `.env` is listed in `.gitignore` so it doesn’t get uploaded to GitHub

## 🧠 How It Works in Code

In `jarvis.py`, we use `python-dotenv` to load the key:

```python
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
