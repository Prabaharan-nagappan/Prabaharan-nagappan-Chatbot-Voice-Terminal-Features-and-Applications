import os
import random
import datetime
from gtts import gTTS
import playsound
import speech_recognition as sr

class RobustVoiceChatbot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.use_voice = self.check_audio_support()
        
        self.responses = {
            "greetings": ["Hello!", "Hi there!", "Greetings!"],
            "farewell": ["Goodbye!", "See you later!"],
            "how_are_you": ["I'm functioning well!", "All systems operational!"],
            "default": ["Interesting.", "Could you rephrase that?"]
        }

    def check_audio_support(self):
        """Check if audio features are available"""
        try:
            # Test if we can even initialize the recognizer
            with sr.Microphone() as source:
                pass
            return True
        except:
            print("Voice input disabled (missing dependencies)")
            return False

    def listen(self):
        """Get user input through voice or text"""
        if self.use_voice:
            try:
                with sr.Microphone() as source:
                    print("\nListening...")
                    audio = self.recognizer.listen(source, timeout=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"You: {text}")
                    return text
            except sr.WaitTimeoutError:
                print("Listening timed out")
            except Exception as e:
                print(f"Voice recognition failed: {e}")
        
        # Fallback to text input
        return input("Type your message: ").lower()

    def speak(self, text):
        """Output through TTS or text"""
        print(f"Bot: {text}")
        
        if self.use_voice:
            try:
                tts = gTTS(text=text, lang='en')
                tts.save("response.mp3")
                playsound.playsound("response.mp3")
                os.remove("response.mp3")
                return
            except Exception as e:
                print(f"Voice output failed: {e}")
        
        # Fallback to text output
        print(f"[Bot would say: {text}]")

    def process_input(self, user_input):
        """Generate appropriate response"""
        if not user_input:
            return random.choice(self.responses["default"])
            
        if any(word in user_input for word in ["hello", "hi"]):
            return random.choice(self.responses["greetings"])
            
        if any(word in user_input for word in ["bye", "exit"]):
            return random.choice(self.responses["farewell"])
            
        if "how are you" in user_input:
            return random.choice(self.responses["how_are_you"])
            
        if "time" in user_input:
            return f"It's {datetime.datetime.now().strftime('%I:%M %p')}"
            
        if "date" in user_input:
            return f"Today is {datetime.datetime.now().strftime('%B %d, %Y')}"
            
        return random.choice(self.responses["default"])

    def run(self):
        """Main conversation loop"""
        self.speak("Voice assistant initialized")
        
        while True:
            user_input = self.listen()
            
            if user_input in ["exit", "quit"]:
                self.speak("Goodbye!")
                break
                
            response = self.process_input(user_input)
            self.speak(response)

if __name__ == "__main__":
    print("Starting Robust Voice Chatbot...")
    
    # Install minimal requirements
    try:
        import speech_recognition
    except ImportError:
        print("Installing SpeechRecognition...")
        import os
        os.system("pip install SpeechRecognition gTTS playsound")
    
    chatbot = RobustVoiceChatbot()
    chatbot.run()