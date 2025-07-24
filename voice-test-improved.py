#!/usr/bin/env python3
"""
Improved voice test - More flexible command matching
"""

import subprocess
import os
import sys

def test_basic_voice():
    print("\n🤖 Jaymi Voice Assistant:")
    print("Commands: 'hello', 'photos', 'system', 'quit'")
    
    while True:
        try:
            command = input("\n💬 Voice Command (type): ").strip().lower()
            
            if command == 'quit' or 'bye' in command:
                speak_response("Goodbye Chuck! I'll be ready when you need me.")
                break
            elif 'hello' in command or 'hi' in command:
                speak_response("Hello Chuck! I'm Jaymi, your personal AI assistant. How can I help you today?")
            elif 'photo' in command or 'picture' in command or 'image' in command:
                speak_response("I found 2 photos in your pictures folder. vacation.jpg and family.png. Would you like me to open them?")
            elif 'system' in command or 'status' in command or 'info' in command:
                speak_response("System status: All systems running normally. Hostname keyfucker, running Linux. ChuckOS voice interface is active!")
            elif 'document' in command or 'file' in command:
                speak_response("I found your resume.pdf and notes.txt in the documents folder. Which would you like to open?")
            else:
                speak_response(f"I heard you say {command}. I'm still learning new commands, but I'm getting smarter every day!")
                
        except KeyboardInterrupt:
            speak_response("Goodbye Chuck!")
            break

def speak_response(text):
    """Make Jaymi speak with personality"""
    print(f"🤖 Jaymi: {text}")
    try:
        subprocess.run(['espeak', '-s', '160', '-p', '60', text], check=False)
    except:
        print("   (TTS not available)")

if __name__ == "__main__":
    print("🚀 ChuckOS Voice Test - Improved")
    print("=================================")
    test_basic_voice()
