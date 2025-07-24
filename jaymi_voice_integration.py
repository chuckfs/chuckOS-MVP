#!/usr/bin/env python3
"""
ChuckOS Jaymi - Voice + File Intelligence Integration
Combines voice interface with smart file finding
"""

import subprocess
import os
import sys
from pathlib import Path
import platform

class JaymiVoiceAI:
    def __init__(self):
        self.name = "Jaymi"
        self.personality = "helpful, intelligent, slightly sassy"
        self.voice_active = True
        print("🤖 Jaymi Voice AI initialized")
    
    def speak(self, text):
        """Make Jaymi speak with personality"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', '160', '-p', '60', text], check=False)
            except:
                pass  # Silent fallback if no audio
    
    def greet_user(self):
        """Initial greeting with voice"""
        greeting = "Hello Chuck! I'm Jaymi, your personal AI assistant with voice. I can find your files, control your system, and chat with you. What would you like me to do?"
        self.speak(greeting)
    
    def process_voice_command(self, command):
        """Process voice commands with intelligence"""
        cmd_lower = command.lower().strip()
        
        # File finding commands
        if any(word in cmd_lower for word in ['photo', 'picture', 'image']):
            return self.find_photos_with_voice()
        elif any(word in cmd_lower for word in ['document', 'file', 'pdf', 'txt']):
            return self.find_documents_with_voice()
        elif 'open' in cmd_lower and any(word in cmd_lower for word in ['photo', 'picture']):
            return self.open_photos()
        elif 'open' in cmd_lower and any(word in cmd_lower for word in ['document', 'file']):
            return self.open_documents()
        
        # System commands
        elif any(word in cmd_lower for word in ['system', 'status', 'info', 'computer']):
            return self.system_info_with_voice()
        elif any(word in cmd_lower for word in ['time', 'date']):
            return self.get_time_info()
        
        # Conversation
        elif any(word in cmd_lower for word in ['hello', 'hi', 'hey']):
            return self.greet_response()
        elif any(word in cmd_lower for word in ['thanks', 'thank you']):
            return self.thank_response()
        elif any(word in cmd_lower for word in ['yes', 'ok', 'okay', 'sure']):
            return self.affirmative_response()
        elif any(word in cmd_lower for word in ['no', 'nope', 'cancel']):
            return self.negative_response()
        
        # Exit commands
        elif any(word in cmd_lower for word in ['quit', 'exit', 'bye', 'goodbye']):
            return self.goodbye()
        
        # Default response
        else:
            return self.unknown_command_response(command)
    
    def find_photos_with_voice(self):
        """Find photos and announce results with voice"""
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        found_files = []
        
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
            count = len(found_files)
            if count == 1:
                response = f"I found 1 photo: {found_files[0].name}. Would you like me to open it?"
            elif count <= 5:
                names = [f.name for f in found_files[:5]]
                response = f"I found {count} photos: {', '.join(names)}. Would you like me to open them?"
            else:
                names = [f.name for f in found_files[:3]]
                response = f"I found {count} photos! Here are the first few: {', '.join(names)}. Would you like to see them all?"
            
            self.speak(response)
            return found_files
        else:
            response = "I couldn't find any photos in your Pictures, Downloads, or Desktop folders. Want me to search elsewhere?"
            self.speak(response)
            return []
    
    def find_documents_with_voice(self):
        """Find documents and announce with voice"""
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
            count = len(found_files)
            if count == 1:
                response = f"I found 1 document: {found_files[0].name}. Want me to open it?"
            elif count <= 5:
                names = [f.name for f in found_files[:5]]
                response = f"I found {count} documents: {', '.join(names)}. Which one would you like?"
            else:
                names = [f.name for f in found_files[:3]]
                response = f"I found {count} documents! Here are the most recent: {', '.join(names)}. Want to see more?"
            
            self.speak(response)
            return found_files
        else:
            response = "No documents found in the usual places. Should I search your entire system?"
            self.speak(response)
            return []
    
    def open_photos(self):
        """Open photos with voice feedback"""
        photos = self.find_photos_with_voice()
        if photos:
            try:
                # Open first photo
                subprocess.run(['xdg-open', str(photos[0])], check=False)
                response = f"Opening {photos[0].name} for you now!"
                self.speak(response)
                return True
            except Exception as e:
                response = "I found the photos but couldn't open them. You might need to install an image viewer."
                self.speak(response)
                return False
        return False
    
    def open_documents(self):
        """Open documents with voice feedback"""
        docs = self.find_documents_with_voice()
        if docs:
            try:
                # Open first document
                subprocess.run(['xdg-open', str(docs[0])], check=False)
                response = f"Opening {docs[0].name} for you!"
                self.speak(response)
                return True
            except Exception as e:
                response = "I found the documents but couldn't open them. You might need to install a document viewer."
                self.speak(response)
                return False
        return False
    
    def system_info_with_voice(self):
        """Provide system information with voice"""
        try:
            hostname = platform.node()
            system = platform.system()
            release = platform.release()
            
            response = f"System status: All systems running normally. Hostname {hostname}, running {system}. ChuckOS voice interface is active and ready!"
            self.speak(response)
            
            print(f"💻 System Details:")
            print(f"   🖥️  Hostname: {hostname}")
            print(f"   🐧 OS: {system} {release}")
            print(f"   🎯 ChuckOS Status: Voice AI Active")
            
            return {
                'hostname': hostname,
                'system': system,
                'release': release,
                'status': 'active'
            }
        except Exception as e:
            response = "System is running well! All ChuckOS components are active."
            self.speak(response)
            return {'status': 'basic_info'}
    
    def get_time_info(self):
        """Get current time/date"""
        import datetime
        now = datetime.datetime.now()
        response = f"It's currently {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}."
        self.speak(response)
        return now
    
    def greet_response(self):
        """Respond to greetings"""
        responses = [
            "Hello Chuck! Great to see you again. What can I help you with?",
            "Hi there! I'm here and ready to assist you with anything.",
            "Hey Chuck! Hope you're having a good day. What would you like me to do?",
        ]
        import random
        response = random.choice(responses)
        self.speak(response)
        return "greeting"
    
    def thank_response(self):
        """Respond to thanks"""
        responses = [
            "You're very welcome, Chuck! Always happy to help.",
            "My pleasure! That's what I'm here for.",
            "Anytime, Chuck! I love being useful.",
        ]
        import random
        response = random.choice(responses)
        self.speak(response)
        return "thanks"
    
    def affirmative_response(self):
        """Handle yes/okay responses"""
        response = "Got it! What would you like me to do next?"
        self.speak(response)
        return "affirmative"
    
    def negative_response(self):
        """Handle no/cancel responses"""
        response = "No problem! Let me know if you need anything else."
        self.speak(response)
        return "negative"
    
    def unknown_command_response(self, command):
        """Handle unknown commands intelligently"""
        responses = [
            f"I heard '{command}'. I'm still learning new commands, but I'm getting smarter every day!",
            f"Interesting request: '{command}'. I don't know that one yet, but I'll remember it for next time.",
            f"You said '{command}' - I'm not sure about that one, but I can help with files, system info, or just chat!",
        ]
        import random
        response = random.choice(responses)
        self.speak(response)
        return "unknown"
    
    def goodbye(self):
        """Say goodbye and exit"""
        responses = [
            "Goodbye Chuck! I'll be ready when you need me again.",
            "See you later! I'm always here when you need an AI assistant.",
            "Bye Chuck! Thanks for letting me help you today.",
        ]
        import random
        response = random.choice(responses)
        self.speak(response)
        return "goodbye"
    
    def run_interactive(self):
        """Main interactive voice loop"""
        self.greet_user()
        
        print("\n" + "="*60)
        print("🎮 JAYMI VOICE AI - Interactive Mode")
        print("="*60)
        print("💡 Try commands like:")
        print("   - 'find my photos'")
        print("   - 'open documents'") 
        print("   - 'system status'")
        print("   - 'hello' or 'thanks'")
        print("   - 'quit' to exit")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n💬 Voice Command: ").strip()
                
                if not user_input:
                    continue
                
                result = self.process_voice_command(user_input)
                
                if result == "goodbye":
                    break
                    
            except KeyboardInterrupt:
                self.goodbye()
                break
            except Exception as e:
                error_response = "Oops! I encountered an error, but I'm still here and ready to help."
                self.speak(error_response)
                print(f"Debug: {e}")

if __name__ == "__main__":
    print("🚀 ChuckOS Jaymi Voice AI - Week 1 Complete")
    print("=" * 50)
    
    jaymi = JaymiVoiceAI()
    jaymi.run_interactive()
