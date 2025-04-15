# Prabaharan-nagappan-Chatbot-Voice-Terminal-Features-and-Applications
Here's a basic Python voice chatbot that doesn't require any external API services (like OpenAI):

# Voice Chatbot Terminal

A simple voice-enabled chatbot that works with or without audio hardware dependencies.

## Features

- Voice input/output (when dependencies are available)
- Automatic fallback to text input/output
- Basic conversational responses
- Time and date queries
- No external API dependencies
- Easy to extend with custom responses

## Setup Instructions

### Prerequisites

- Python 3.6+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Prabaharan-nagappan/Prabaharan-nagappan-Chatbot-Voice-Terminal-Features-and-Applications.git
cd 
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Alternative Installation (if requirements.txt fails)

For minimal installation:
```bash
pip install SpeechRecognition gTTS playsound
```

For full functionality (on Linux/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-dev espeak
pip install pyaudio pyttsx3 SpeechRecognition gTTS playsound
```

## Usage

Run the chatbot:
```bash
python chatbot.py
```

### Interaction Modes

1. **Voice Mode** (if supported):
   - Speak to the chatbot using your microphone
   - The chatbot will respond with synthesized voice

2. **Text Mode** (fallback):
   - If voice input isn't available, type your messages
   - Responses will be printed to console

### Basic Commands

- "hello"/"hi" - Greet the bot
- "how are you" - Get bot status
- "what time is it" - Get current time
- "what's today's date" - Get current date
- "exit"/"quit" - End the session

## Configuration

Edit `chatbot.py` to:
- Add custom responses in the `self.responses` dictionary
- Modify voice parameters (rate, volume)
- Add new command handlers in `process_input()`

## Troubleshooting

### Common Issues

1. **"No module named pyaudio"**
   - Use the text fallback mode, or install system dependencies:
   ```bash
   sudo apt-get install portaudio19-dev python3-dev
   pip install pyaudio
   ```

2. **"aplay/espeak not found"**
   - The system will automatically fall back to gTTS (requires internet)
   - For offline use on Linux:
   ```bash
   sudo apt-get install espeak
   ```

3. **Microphone not working**
   - Check your audio input settings
   - Use text input mode if microphone is unavailable

## Extending the Chatbot

To add new features:

1. Add new response categories to `self.responses`
2. Add new condition checks in `process_input()`
3. Implement new utility functions as needed

Example extension for weather:
```python
if "weather" in user_input:
    return "I'm sorry, I can't check weather yet. This feature can be added!"
```

## License

MIT License - Free for personal and commercial use

---

This README provides comprehensive setup and usage instructions while accounting for different environments and potential issues. The chatbot is designed to work in most scenarios, falling back gracefully when dependencies are missing.
