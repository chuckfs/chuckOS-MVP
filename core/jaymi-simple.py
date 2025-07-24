#!/usr/bin/env python3
"""
ChuckOS MVP - Jaymi AI Assistant (Simple Text-Only Version)
For initial testing without speech dependencies
"""

import os
import sys
from pathlib import Path
import json
import subprocess

class JaymiSimple:
    def __init__(self):
        self.name = "Jaymi"
        self.personality = "helpful, witty, slightly sassy"
        print("🤖 Jaymi AI initialized (text-only mode)")
    
    def greet_user(self):
        """Initial greeting with personality"""
        greeting = """
🌟 Hello there! I'm Jaymi, your personal AI assistant.
💫 I'm currently in text-only mode while we test the core systems.
🎯 I can help you find files, get system info, and chat!

Try commands like:
- "find my photos"
- "find my documents" 
- "system info"
- or just chat with me!
        """
        print(greeting)
    
    def process_command(self, user_input):
        """Process natural language commands"""
        input_lower = user_input.lower()
        
        if "find" in input_lower and ("photo" in input_lower or "image" in input_lower):
            return self.find_photos(user_input)
        elif "find" in input_lower and "document" in input_lower:
            return self.find_documents(user_input)
        elif "system" in input_lower or "computer" in input_lower:
            return self.system_info()
        elif "quit" in input_lower or "exit" in input_lower:
            return "quit"
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
            print(f"🎉 I found {len(found_files)} photos! Here are the most recent ones:")
            
            # Show first 5 files
            for i, file in enumerate(found_files[:5], 1):
                print(f"  📸 {i}. {file.name} - {file.parent}")
            
            if len(found_files) > 5:
                print(f"  ... and {len(found_files) - 5} more!")
            
            return found_files
        else:
            print("🤔 I couldn't find any photos in Pictures, Downloads, or Desktop.")
            print("💡 Try putting some images in those folders and ask again!")
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
            print(f"📄 Found {len(found_files)} documents for you!")
            
            for i, file in enumerate(found_files[:5], 1):
                print(f"  📄 {i}. {file.name} - {file.parent}")
            
            if len(found_files) > 5:
                print(f"  ... and {len(found_files) - 5} more!")
            
            return found_files
        else:
            print("🤔 No documents found in the usual places.")
            print("💡 Want me to search elsewhere?")
            return []
    
    def system_info(self):
        """Provide system information"""
        try:
            import platform
            hostname = platform.node()
            system = platform.system()
            release = platform.release()
            
            print(f"💻 System Info:")
            print(f"  🖥️  Hostname: {hostname}")
            print(f"  🐧 OS: {system} {release}")
            print(f"  🎯 ChuckOS MVP Status: Running!")
            
            return f"System: {hostname} running {system} {release}"
        except Exception as e:
            print("💻 I can see this system is running well!")
            return "system_info_basic"
    
    def chat_response(self, user_input):
        """Generate conversational response"""
        responses = [
            "That's interesting! Tell me more. 💭",
            "I'm here to help with whatever you need! 🚀",
            "Sounds good! What else can I do for you? ✨",
            "I love chatting with you! What's on your mind? 💫",
            "Let me know if you need help finding files or getting system info! 🔍"
        ]
        
        import random
        response = random.choice(responses)
        print(f"🤖 {response}")
        return response
    
    def run_interactive(self):
        """Main interactive loop"""
        self.greet_user()
        
        print("\n" + "="*50)
        print("🎮 INTERACTIVE MODE - Type your commands!")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                result = self.process_command(user_input)
                
                if result == "quit":
                    print("\n🌟 Goodbye! Thanks for testing ChuckOS MVP!")
                    print("💰 Next: Add voice interface and polish for $299 launch!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n🌟 Goodbye! Thanks for testing ChuckOS MVP!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("🔧 Don't worry, we're still in MVP development!")

if __name__ == "__main__":
    jaymi = JaymiSimple()
    jaymi.run_interactive()
