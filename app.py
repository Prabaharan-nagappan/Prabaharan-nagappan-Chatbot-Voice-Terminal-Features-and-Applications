from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import speech_recognition as sr
from gtts import gTTS
import datetime
import random
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'audio'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Responses database
RESPONSES = {
    "greetings": ["Hello!", "Hi there!", "Greetings!"],
    "farewell": ["Goodbye!", "See you later!", "Bye bye!"],
    "how_are_you": ["I'm doing well, thanks!", "All systems operational!"],
    "default": ["Interesting, tell me more.", "I didn't catch that."]
}

def process_text_input(text):
    text = text.lower()
    
    if not text:
        return random.choice(RESPONSES["default"])
        
    if any(word in text for word in ["hello", "hi", "hey"]):
        return random.choice(RESPONSES["greetings"])
        
    if any(word in text for word in ["bye", "goodbye"]):
        return random.choice(RESPONSES["farewell"])
        
    if "how are you" in text:
        return random.choice(RESPONSES["how_are_you"])
        
    if "time" in text:
        return f"It's {datetime.datetime.now().strftime('%I:%M %p')}"
        
    if "date" in text:
        return f"Today is {datetime.datetime.now().strftime('%B %d, %Y')}"
        
    return random.choice(RESPONSES["default"])

def text_to_speech(text):
    """Convert text to speech and return audio file path"""
    tts = gTTS(text=text, lang='en')
    filename = secure_filename(f"response_{datetime.datetime.now().timestamp()}.mp3")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    tts.save(filepath)
    return filename

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get input from form or JSON
    if request.form.get('text'):
        user_input = request.form.get('text')
    elif request.json and 'text' in request.json:
        user_input = request.json['text']
    else:
        return jsonify({"error": "No input provided"}), 400
    
    # Process input
    response_text = process_text_input(user_input)
    audio_file = text_to_speech(response_text)
    
    return jsonify({
        "text": response_text,
        "audio": f"/audio/{audio_file}"
    })

@app.route('/api/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400
        
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if audio_file:
        # Save the original file
        original_filename = secure_filename(f"user_audio_{datetime.datetime.now().timestamp()}.webm")
        original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        audio_file.save(original_filepath)
        
        # Convert to WAV format
        wav_filename = secure_filename(f"user_audio_{datetime.datetime.now().timestamp()}.wav")
        wav_filepath = os.path.join(app.config['UPLOAD_FOLDER'], wav_filename)
        
        try:
            # Convert using ffmpeg
            subprocess.run([
                'ffmpeg', '-i', original_filepath,
                '-acodec', 'pcm_s16le',
                '-ac', '1',
                '-ar', '16000',
                wav_filepath
            ], check=True)
            
            # Process the converted WAV file
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_filepath) as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio)
                    response_text = process_text_input(text)
                    response_audio = text_to_speech(response_text)
                    
                    return jsonify({
                        "text": response_text,
                        "audio": f"/audio/{response_audio}"
                    })
                except sr.UnknownValueError:
                    return jsonify({"error": "Could not understand audio"}), 400
                except sr.RequestError:
                    return jsonify({"error": "Speech service unavailable"}), 503
                    
        except subprocess.CalledProcessError:
            return jsonify({"error": "Failed to process audio file"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)