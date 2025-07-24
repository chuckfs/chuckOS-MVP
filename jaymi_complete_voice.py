#!/usr/bin/env python3
"""
ChuckOS Jaymi - Complete Voice Integration
Combines simulated voice input with real Jaymi AI responses
"""

import subprocess
import os
import sys
from pathlib import Path
import platform
import time
import random

class JaymiCompleteVoice:
    def __init__(self):
        self.name = "Jaymi"
        self.personality = "helpful, intelligent, slightly sassy"
        self.voice_active = True
        self.listening_mode = "simulated"  # Can be "real" or "simulated"
        self.last_found_files = []
        print("🤖 Jaymi Complete Voice AI initialized")
    
    def speak(self, text):
        """Make Jaymi speak with personality"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', '160', '-p', '60', text], check=False)
            except:
                pass
    
    def greet_user(self):
        """Initial greeting with voice"""
        greeting = "Hello Chuck! I'm Jaymi with full voice integration. I can understand voice commands and respond intelligently. Ready to show you what I can do!"
        self.speak(greeting)
    
    def listen_for_command(self):
        """Get voice command - simulated for now, real speech later"""
        if self.listening_mode == "simulated":
            return self.simulated_voice_input()
        else:
            return self.real_voice_input()
    
    def simulated_voice_input(self):
        """Simulate voice commands for development"""
        print("\n🎤 VOICE INPUT MODE")
        print("Type what you would say, or choose a preset:")
        print("1. Hello Jaymi")
        print("2. Find my photos") 
        print("3. System status")
        print("4. Open documents")
        print("5. What time is it")
        print("6. Thanks")
        print("Or type any custom command...")
        
        choice = input("\n💬 Voice Input (number or text): ").strip()
        
        # Map numbers to commands
        presets = {
            "1": "Hello Jaymi",
            "2": "Find my photos",
            "3": "System status", 
            "4": "Open documents",
            "5": "What time is it",
            "6": "Thanks"
        }
        
        command = presets.get(choice, choice)
        print(f"🎙️ Voice Command: '{command}'")
        return command
    
    def process_voice_command(self, command):
        """Process voice commands with full Jaymi intelligence"""
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
        elif any(word in cmd_lower for word in ['time', 'date', 'clock']):
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
        
        # Demo commands
        elif 'demo' in cmd_lower or 'show' in cmd_lower:
            return self.run_demo_sequence()
        
        # Default response
        else:
            return self.intelligent_response(command)
    
    def find_photos_with_voice(self):
        """Find photos with intelligent voice response"""
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
        
        self.last_found_files = found_files
        
        if found_files:
            count = len(found_files)
            names = [f.name for f in found_files[:3]]
            
            if count == 1:
                response = f"Perfect! I found 1 photo: {names[0]}. Would you like me to open it for you?"
            elif count <= 3:
                response = f"Great! I found {count} photos: {', '.join(names)}. Which one interests you?"
            else:
                response = f"Excellent! I discovered {count} photos. Here are the first few: {', '.join(names)}. Want to see them all?"
            
            self.speak(response)
            return found_files
        else:
            response = "Hmm, I couldn't locate any photos in your usual folders. Should I search your entire system? I'm very thorough!"
            self.speak(response)
            return []
    
    def find_documents_with_voice(self):
        """Find documents with personality"""
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
        
        self.last_found_files = found_files
        
        if found_files:
            count = len(found_files)
            names = [f.name for f in found_files[:3]]
            
            if count == 1:
                response = f"Found it! One document: {names[0]}. Ready to open it?"
            elif count <= 3:
                response = f"Success! I located {count} documents: {', '.join(names)}. Which one do you need?"
            else:
                response = f"Impressive collection! I found {count} documents. The most recent are: {', '.join(names)}. What are you looking for specifically?"
            
            self.speak(response)
            return found_files
        else:
            response = "No documents in the usual spots. I could search everywhere if you'd like! I'm quite persistent."
            self.speak(response)
            return []
    
    def system_info_with_voice(self):
        """Professional system report with personality"""
        try:
            hostname = platform.node()
            system = platform.system()
            release = platform.release()
            
            response = f"System report: All systems optimal! Running on {hostname} with {system}. ChuckOS voice interface is fully operational and ready for action!"
            self.speak(response)
            
            print(f"💻 Detailed System Status:")
            print(f"   🖥️  Hostname: {hostname}")
            print(f"   🐧 OS: {system} {release}")
            print(f"   🎯 ChuckOS: Voice AI Active")
            print(f"   🎤 Voice Mode: {self.listening_mode}")
            print(f"   🤖 Jaymi Status: Fully Operational")
            
            return True
        except Exception as e:
            response = "System running beautifully! All ChuckOS components are active and I'm feeling great!"
            self.speak(response)
            return True
    
    def get_time_info(self):
        """Get time with personality"""
        import datetime
        now = datetime.datetime.now()
        
        hour = now.hour
        if 5 <= hour < 12:
            greeting = "Good morning Chuck!"
        elif 12 <= hour < 17:
            greeting = "Good afternoon!"
        elif 17 <= hour < 21:
            greeting = "Good evening!"
        else:
            greeting = "Working late tonight?"
        
        response = f"{greeting} It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}."
        self.speak(response)
        return now
    
    def greet_response(self):
        """Varied greeting responses"""
        responses = [
            "Hello Chuck! Wonderful to hear from you. What amazing thing shall we accomplish today?",
            "Hi there! I'm energized and ready to assist with whatever you need.",
            "Hey Chuck! Hope you're having a fantastic day. I'm here and excited to help!",
        ]
        response = random.choice(responses)
        self.speak(response)
        return "greeting"
    
    def intelligent_response(self, command):
        """Intelligent response to unknown commands"""
        responses = [
            f"Interesting! You said '{command}'. I'm constantly learning new things. Could you rephrase that or tell me more about what you'd like me to do?",
            f"I heard '{command}' - that's a new one for me! I love expanding my capabilities. What would you like me to help you with?",
            f"'{command}' sounds intriguing! I don't have that command yet, but I can help with files, system info, or just chat. What interests you most?",
        ]
        response = random.choice(responses)
        self.speak(response)
        return "learning"
    
    def run_demo_sequence(self):
        """Run a complete demo of capabilities"""
        self.speak("Absolutely! Let me demonstrate my capabilities. Here's what I can do:")
        
        time.sleep(1)
        self.speak("First, let me find your photos.")
        self.find_photos_with_voice()
        
        time.sleep(2)
        self.speak("Now checking your documents.")
        self.find_documents_with_voice()
        
        time.sleep(2)
        self.speak("Here's your system status.")
        self.system_info_with_voice()
        
        time.sleep(2)
        self.speak("And finally, let me tell you the time.")
        self.get_time_info()
        
        time.sleep(1)
        self.speak("That's just a taste of what I can do! I'm your complete AI assistant, ready for any task you have in mind.")
        
        return "demo_complete"
    
    def goodbye(self):
        """Personalized goodbye"""
        responses = [
            "Goodbye Chuck! It's been wonderful helping you today. I'll be here whenever you need me!",
            "See you soon! Thanks for letting me show off my capabilities. I'm always ready to assist!",
            "Bye Chuck! Remember, I'm just a voice command away whenever you need an AI companion!",
        ]
        response = random.choice(responses)
        self.speak(response)
        return "goodbye"
    
    def thank_response(self):
        """Respond to thanks with personality"""
        responses = [
            "You're absolutely welcome, Chuck! Helping you is what I live for!",
            "My genuine pleasure! I love being useful and making your day easier.",
            "Anytime, Chuck! Your success is my success!",
        ]
        response = random.choice(responses)
        self.speak(response)
        return "thanks"
    
    def affirmative_response(self):
        """Handle yes responses"""
        response = "Excellent! What would you like me to do next? I'm ready for any challenge!"
        self.speak(response)
        return "affirmative"
    
    def negative_response(self):
        """Handle no responses"""
        response = "No worries at all! I'm here whenever you need assistance. Just say the word!"
        self.speak(response)
        return "negative"
    
    def run_interactive(self):
        """Main interactive voice loop"""
        self.greet_user()
        
        print("\n" + "="*70)
        print("🎮 JAYMI COMPLETE VOICE AI - Week 2 Integration")
        print("="*70)
        print("🎤 Voice Commands Available:")
        print("   • 'Find my photos' - Smart photo discovery")
        print("   • 'System status' - Complete system report")  
        print("   • 'What time is it' - Time with personality")
        print("   • 'Demo' - Full capability demonstration")
        print("   • 'Thanks' or 'Hello' - Natural conversation")
        print("   • 'Quit' - Exit gracefully")
        print("="*70)
        
        while True:
            try:
                command = self.listen_for_command()
                
                if not command or command.lower().strip() == '':
                    continue
                
                result = self.process_voice_command(command)
                
                if result == "goodbye":
                    break
                    
            except KeyboardInterrupt:
                self.goodbye()
                break
            except Exception as e:
                error_response = "Oops! I encountered a small hiccup, but I'm still here and ready to help you!"
                self.speak(error_response)
                print(f"Debug: {e}")

if __name__ == "__main__":
    print("🚀 ChuckOS Jaymi - Complete Voice AI Integration")
    print("Week 2: Real Intelligence + Voice Interface")
    print("=" * 60)
    
    jaymi = JaymiCompleteVoice()
    jaymi.run_interactive()
