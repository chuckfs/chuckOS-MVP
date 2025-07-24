#!/usr/bin/env python3
"""
Quick voice test for ChuckOS - No complex dependencies
"""

import subprocess
import os
import sys

def test_text_to_speech():
    """Test if we can make Jaymi speak"""
    print("🎤 Testing Text-to-Speech...")
    try:
        # Use system espeak (already installed)
        subprocess.run(['espeak', '-s', '150', 'Hello Chuck! I am Jaymi, your AI assistant.'], check=True)
        print("✅ Text-to-Speech working!")
        return True
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return False

def test_basic_voice():
    """Test basic voice interaction without complex speech recognition"""
    print("\n🤖 Basic Voice Test:")
    print("Type commands to test Jaymi's responses:")
    print("Commands: 'hello', 'find photos', 'system info', 'quit'")
    
    while True:
        try:
            command = input("\n💬 Voice Command (type): ").strip().lower()
            
            if command == 'quit':
                speak_response("Goodbye Chuck! I'll be ready when you need me.")
                break
            elif 'hello' in command:
                speak_response("Hello Chuck! I'm Jaymi, your personal AI assistant. How can I help you today?")
            elif 'find photos' in command:
                speak_response("I found 2 photos in your pictures folder. Would you like me to open them?")
            elif 'system info' in command:
                speak_response("System status: All systems running normally. You're on hostname keyfucker running Linux.")
            else:
                speak_response("I understand you want me to help with that. I'm still learning new commands.")
                
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
    print("🚀 ChuckOS Voice Test - Week 1")
    print("================================")
    
    if test_text_to_speech():
        print("\n🎯 Voice system is working! Testing interaction...")
        test_basic_voice()
    else:
        print("\n🔧 Let's fix the audio system first.")
        print("Run: sudo apt install espeak-ng")
