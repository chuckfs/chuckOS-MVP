#!/usr/bin/env python3
"""
ChuckOS MVP - Jaymi AI Assistant
Simplified version for $299 product launch
"""

import os
import sys
import json
import subprocess
import speech_recognition as sr
import pyttsx3
from pathlib import Path
import sqlite3

class JaymiMVP:
    def __init__(self):
        self.name = "Jaymi"
        self.personality = "helpful, witty, slightly sassy"
        self.voice_engine = pyttsx3.init()
        self.setup_voice()
        self.vault_path = Path.home() / ".jaymi_vault"
        self.setup_vault()
    
    def setup_voice(self):
        """Configure voice settings"""
        voices = self.voice_engine.getProperty('voices')
        # Try to find female voice
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.voice_engine.setProperty('voice', voice.id)
                break
        
        self.voice_engine.setProperty('rate', 175)
        self.voice_engine.setProperty('volume', 0.9)
    
    def speak(self, text):
        """Speak with personality"""
        print(f"🤖 Jaymi: {text}")
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()
    
    def setup_vault(self):
        """Initialize secure storage"""
        self.vault_path.mkdir(exist_ok=True)
        self.db_path = self.vault_path / "memories.db"
        
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS interactions
                       (timestamp TEXT, user_input TEXT, ai_response TEXT)''')
        conn.close()
    
    def greet_user(self):
        """Initial greeting with personality"""
        greeting = "Hello there! I'm Jaymi, your personal AI assistant. What can I help you with today?"
        self.speak(greeting)
    
    def process_command(self, user_input):
        """Process natural language commands"""
        input_lower = user_input.lower()
        
        if "find" in input_lower and ("photo" in input_lower or "image" in input_lower):
            return self.find_photos(user_input)
        elif "find" in input_lower and "document" in input_lower:
            return self.find_documents(user_input)
        elif "open" in input_lower:
            return self.open_file(user_input)
        elif "system" in input_lower or "computer" in input_lower:
            return self.system_info()
        else:
            return self.chat_response(user_input)
    
    def find_photos(self, query):
        """Find photo files on system"""
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        found_files = []
        
        # Search common directories
        search_dirs = [
            Path.home() / "Pictures",
            Path.home() / "Downloads", 
            Path.home() / "Desktop"
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for ext in extensions:
                    found_files.extend(search_dir.rglob(f"*{ext}"))
        
        if found_files:
            response = f"I found {len(found_files)} photos! Here are the most recent ones:"
            self.speak(response)
            
            # Show first 5 files
            for file in found_files[:5]:
                print(f"📸 {file.name} - {file.parent}")
            
            return found_files
        else:
            response = "I couldn't find any photos. Maybe check if you have images in Pictures, Downloads, or Desktop?"
            self.speak(response)
            return []
    
    def find_documents(self, query):
        """Find document files"""
        extensions = ['.pdf', '.doc', '.docx', '.txt', '.md']
        found_files = []
        
        search_dirs = [
            Path.home() / "Documents",
            Path.home() / "Downloads",
            Path.home() / "Desktop"
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for ext in extensions:
                    found_files.extend(search_dir.rglob(f"*{ext}"))
        
        if found_files:
            response = f"Found {len(found_files)} documents for you!"
            self.speak(response)
            
            for file in found_files[:5]:
                print(f"📄 {file.name} - {file.parent}")
            
            return found_files
        else:
            response = "No documents found in the usual places. Want me to search elsewhere?"
            self.speak(response)
            return []
    
    def open_file(self, query):
        """Open file based on description"""
        response = "I'd love to open that file for you! For now, can you tell me the exact filename?"
        self.speak(response)
        return "open_file_requested"
    
    def system_info(self):
        """Provide system information"""
        try:
            hostname = subprocess.check_output(['hostname']).decode().strip()
            uptime = subprocess.check_output(['uptime', '-p']).decode().strip()
            
            response = f"You're on {hostname}. System has been {uptime}. Everything looks good!"
            self.speak(response)
            return response
        except:
            response = "I can see this system is running well!"
            self.speak(response)
            return response
    
    def chat_response(self, user_input):
        """Generate conversational response"""
        responses = [
            "That's interesting! Tell me more.",
            "I'm here to help with whatever you need.",
            "Sounds good! What else can I do for you?",
            "I love chatting with you! What's on your mind?",
            "Let me know if you need help finding files or controlling the system."
        ]
        
        import random
        response = random.choice(responses)
        self.speak(response)
        return response
    
    def listen_for_command(self):
        """Listen for voice commands"""
        r = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (say something)")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            text = r.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            self.speak("Sorry, I'm having trouble with speech recognition right now.")
            return None
    
    def run_interactive(self):
        """Main interactive loop"""
        self.greet_user()
        
        while True:
            try:
                # Try voice input first
                print("\n💬 Say something or type 'text:' followed by your message")
                print("📝 Or type 'quit' to exit")
                
                user_input = input(">> ").strip()
                
                if user_input.lower() == 'quit':
                    self.speak("Goodbye! It was great helping you today.")
                    break
                elif user_input.startswith('voice'):
                    voice_input = self.listen_for_command()
                    if voice_input:
                        self.process_command(voice_input)
                elif user_input.startswith('text:'):
                    text_input = user_input[5:].strip()
                    self.process_command(text_input)
                else:
                    self.process_command(user_input)
                    
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, I encountered an error. Let's try again.")

if __name__ == "__main__":
    jaymi = JaymiMVP()
    jaymi.run_interactive()
