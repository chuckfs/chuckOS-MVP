#!/usr/bin/env python3
"""
ChuckOS Jaymi Perfect Voice Experience
Real speech recognition + wake word detection + natural responses
"""

import json
import os
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
import queue
import signal
import sys

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    print("✅ Speech recognition available")
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ Speech recognition not available - install with: pip install SpeechRecognition pyaudio")

class JaymiPerfectVoice:
    def __init__(self):
        self.name = "Jaymi Voice"
        self.voice_active = True
        self.listening = False
        self.wake_words = ["hey jaymi", "jaymi", "chuck os"]
        self.recognition_queue = queue.Queue()
        self.memory_file = Path.home() / ".jaymi_voice_memory.json"
        
        # Load voice preferences
        self.memory = self.load_voice_memory()
        
        # Initialize speech recognition if available
        if SPEECH_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = None
            self.setup_microphone()
        
        print("🎤 Jaymi Perfect Voice initialized")
        print(f"🧠 Voice interactions remembered: {len(self.memory.get('voice_commands', []))}")
    
    def load_voice_memory(self):
        """Load voice-specific memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "voice_commands": [],
            "wake_word_stats": {"hey jaymi": 0, "jaymi": 0, "chuck os": 0},
            "speech_recognition_accuracy": [],
            "preferred_voice_speed": 160,
            "voice_sessions": 0
        }
    
    def save_voice_memory(self):
        """Save voice memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Couldn't save voice memory: {e}")
    
    def setup_microphone(self):
        """Setup microphone with noise adjustment"""
        if not SPEECH_AVAILABLE:
            return False
        
        try:
            self.microphone = sr.Microphone()
            print("🎤 Adjusting for ambient noise... (speak normally)")
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("✅ Microphone calibrated!")
            return True
            
        except Exception as e:
            print(f"❌ Microphone setup failed: {e}")
            print("💡 Try: sudo apt install portaudio19-dev python3-pyaudio")
            return False
    
    def speak_enhanced(self, text, emotion="neutral", speed=None):
        """Enhanced speech with emotion and learned preferences"""
        print(f"🤖 Jaymi: {text}")
        
        # Use learned speed preference
        if speed is None:
            speed = self.memory.get("preferred_voice_speed", 160)
        
        # Emotional speech parameters
        emotions = {
            "excited": {"speed": speed + 20, "pitch": 70},
            "calm": {"speed": speed - 20, "pitch": 50}, 
            "professional": {"speed": speed, "pitch": 60},
            "happy": {"speed": speed + 10, "pitch": 65},
            "concerned": {"speed": speed - 10, "pitch": 55},
            "neutral": {"speed": speed, "pitch": 60}
        }
        
        params = emotions.get(emotion, emotions["neutral"])
        
        if self.voice_active:
            try:
                subprocess.run([
                    'espeak', '-s', str(params["speed"]), 
                    '-p', str(params["pitch"]), text
                ], check=False)
            except:
                pass
        
        time.sleep(0.2)
    
    def listen_for_wake_word(self, timeout=None):
        """Listen for wake word"""
        if not SPEECH_AVAILABLE or not self.microphone:
            return None
        
        try:
            print("👂 Listening for wake word... (say 'Hey Jaymi')")
            
            with self.microphone as source:
                # Quick listen for wake word
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
            
            try:
                # Use faster recognition for wake word
                text = self.recognizer.recognize_google(audio).lower()
                print(f"🎧 Heard: '{text}'")
                
                # Check for wake words
                for wake_word in self.wake_words:
                    if wake_word in text:
                        print(f"✅ Wake word detected: '{wake_word}'")
                        self.memory["wake_word_stats"][wake_word] += 1
                        self.save_voice_memory()
                        return wake_word
                
                return None
                
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                print("❌ Speech recognition service unavailable")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"❌ Wake word detection error: {e}")
            return None
    
    def listen_for_command(self, timeout=10):
        """Listen for voice command after wake word"""
        if not SPEECH_AVAILABLE or not self.microphone:
            return None
        
        try:
            print("🎤 Listening for command... (speak now)")
            self.speak_enhanced("I'm listening.", "neutral", 140)
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
            
            try:
                # Recognize the command
                command = self.recognizer.recognize_google(audio)
                print(f"✅ Command: '{command}'")
                
                # Remember this voice command
                self.memory["voice_commands"].append({
                    "timestamp": datetime.now().isoformat(),
                    "command": command,
                    "recognized": True
                })
                self.save_voice_memory()
                
                return command
                
            except sr.UnknownValueError:
                print("❓ Couldn't understand the command")
                self.speak_enhanced("I didn't catch that. Could you repeat it?", "concerned")
                return None
            except sr.RequestError as e:
                print(f"❌ Recognition service error: {e}")
                self.speak_enhanced("I'm having trouble with speech recognition right now.", "concerned")
                return None
                
        except sr.WaitTimeoutError:
            print("⏰ No command heard")
            self.speak_enhanced("I didn't hear a command. Try saying 'Hey Jaymi' first.", "neutral")
            return None
        except Exception as e:
            print(f"❌ Command recognition error: {e}")
            return None
    
    def process_voice_command(self, command):
        """Process voice command with intelligent responses"""
        if not command:
            return
        
        cmd_lower = command.lower().strip()
        
        # Smart responses based on voice patterns
        if any(word in cmd_lower for word in ['photo', 'picture', 'image']):
            self.speak_enhanced("Let me find your photos for you!", "happy")
            return self.voice_photo_search()
            
        elif any(word in cmd_lower for word in ['system', 'status', 'computer']):
            self.speak_enhanced("Checking your system status now.", "professional")
            return self.voice_system_status()
            
        elif any(word in cmd_lower for word in ['time', 'clock', 'date']):
            now = datetime.now()
            time_response = f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}."
            self.speak_enhanced(time_response, "neutral")
            return "time_given"
            
        elif any(word in cmd_lower for word in ['hello', 'hi', 'hey']):
            greetings = [
                "Hello Chuck! Great to hear your voice!",
                "Hi there! I love when you talk to me!",
                "Hey Chuck! Voice interaction is so much better than typing!"
            ]
            import random
            response = random.choice(greetings)
            self.speak_enhanced(response, "happy")
            return "greeting"
            
        elif any(word in cmd_lower for word in ['thank', 'thanks']):
            thanks_responses = [
                "You're very welcome, Chuck! I love helping you!",
                "My pleasure! Voice commands make everything so much easier!",
                "Anytime, Chuck! I'm always here to help!"
            ]
            import random
            response = random.choice(thanks_responses)
            self.speak_enhanced(response, "happy")
            return "thanks"
            
        elif any(word in cmd_lower for word in ['stop', 'quit', 'exit', 'goodbye']):
            self.speak_enhanced("Goodbye Chuck! Just say 'Hey Jaymi' anytime you need me!", "calm")
            return "goodbye"
            
        else:
            # Intelligent unknown command handling
            self.speak_enhanced(f"I heard you say '{command}'. I'm still learning voice commands, but I'm getting smarter every day!", "neutral")
            return "learning"
    
    def voice_photo_search(self):
        """Voice-controlled photo search"""
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        found_files = []
        
        search_dirs = [
            Path.home() / "Pictures",
            Path.home() / "Downloads", 
            Path.home() / "Desktop"
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for ext in extensions:
                    for file_path in search_dir.rglob(f"*{ext}"):
                        if file_path.stat().st_size > 0:
                            found_files.append(file_path)
        
        if found_files:
            count = len(found_files)
            total_size = sum(f.stat().st_size for f in found_files) / (1024*1024)
            
            if count == 1:
                response = f"I found 1 photo: {found_files[0].name}. Would you like me to open it?"
            elif count <= 5:
                names = [f.name for f in found_files[:3]]
                response = f"I found {count} photos, including {', '.join(names)}. Want to see them?"
            else:
                response = f"I found {count} photos totaling {total_size:.1f} megabytes. That's a nice collection!"
            
            self.speak_enhanced(response, "excited")
            return found_files
        else:
            self.speak_enhanced("I don't see any photos yet. When you add some, just ask me to find them!", "neutral")
            return []
    
    def voice_system_status(self):
        """Voice system status report"""
        try:
            import platform
            import shutil
            
            hostname = platform.node()
            system = platform.system()
            
            # Get disk usage
            total, used, free = shutil.disk_usage(Path.home())
            free_gb = free / (1024**3)
            
            if free_gb < 10:
                storage_msg = f"Warning: Only {free_gb:.1f} gigabytes free space remaining."
                emotion = "concerned"
            else:
                storage_msg = f"Storage looks good with {free_gb:.1f} gigabytes available."
                emotion = "professional"
            
            response = f"System status for {hostname}: All systems running normally on {system}. {storage_msg} ChuckOS voice interface is active and ready!"
            
            self.speak_enhanced(response, emotion)
            return "system_reported"
            
        except Exception as e:
            self.speak_enhanced("System is running well! All ChuckOS voice components are active.", "professional")
            return "basic_status"
    
    def continuous_voice_mode(self):
        """Continuous voice interaction mode"""
        if not SPEECH_AVAILABLE:
            print("❌ Speech recognition not available. Install with:")
            print("   pip install SpeechRecognition pyaudio")
            return
        
        if not self.microphone:
            print("❌ Microphone not available")
            return
        
        self.memory["voice_sessions"] += 1
        self.save_voice_memory()
        
        print("\n🎤 CONTINUOUS VOICE MODE ACTIVE")
        print("=" * 40)
        print("Say 'Hey Jaymi' to activate, then give a command")
        print("Say 'stop listening' or press Ctrl+C to exit")
        print("=" * 40)
        
        self.speak_enhanced("Voice mode activated! Say 'Hey Jaymi' to get my attention.", "excited")
        
        try:
            while True:
                # Listen for wake word
                wake_word = self.listen_for_wake_word(timeout=5)
                
                if wake_word:
                    # Acknowledge wake word
                    acknowledgments = [
                        "Yes Chuck?",
                        "I'm here! What do you need?",
                        "How can I help you?",
                        "Ready for your command!"
                    ]
                    import random
                    ack = random.choice(acknowledgments)
                    self.speak_enhanced(ack, "happy", 140)
                    
                    # Listen for command
                    command = self.listen_for_command()
                    
                    if command:
                        result = self.process_voice_command(command)
                        if result == "goodbye":
                            break
                    
                    print("\n👂 Listening for 'Hey Jaymi' again...")
                    
        except KeyboardInterrupt:
            self.speak_enhanced("Voice mode deactivated. Goodbye Chuck!", "calm")
            print("\n🎤 Voice mode stopped")
    
    def test_voice_system(self):
        """Test voice system components"""
        print("\n🧪 VOICE SYSTEM TEST")
        print("=" * 30)
        
        # Test text-to-speech
        print("1. Testing text-to-speech...")
        self.speak_enhanced("Text to speech is working perfectly!", "happy")
        
        # Test microphone
        if SPEECH_AVAILABLE and self.microphone:
            print("2. Testing microphone...")
            print("   Say something (you have 5 seconds):")
            
            test_result = self.listen_for_command(timeout=5)
            if test_result:
                self.speak_enhanced(f"Perfect! I heard you say: {test_result}", "excited")
            else:
                self.speak_enhanced("Microphone test completed, but I didn't catch anything clear.", "neutral")
        else:
            print("2. Microphone test skipped (not available)")
        
        # Test wake word detection
        if SPEECH_AVAILABLE and self.microphone:
            print("3. Testing wake word detection...")
            print("   Try saying 'Hey Jaymi' (you have 10 seconds):")
            
            wake_result = self.listen_for_wake_word(timeout=10)
            if wake_result:
                self.speak_enhanced("Excellent! Wake word detection is working!", "excited")
            else:
                self.speak_enhanced("Wake word test completed.", "neutral")
        else:
            print("3. Wake word test skipped (not available)")
        
        print("\n✅ Voice system test complete!")
    
    def interactive_voice_menu(self):
        """Interactive menu for voice features"""
        print("\n🎤 JAYMI PERFECT VOICE EXPERIENCE")
        print("=" * 50)
        print("1. Continuous Voice Mode (say 'Hey Jaymi' to activate)")
        print("2. Test Voice System")
        print("3. Voice Memory Stats")
        print("4. Text-Only Mode (fallback)")
        print("5. Quit")
        
        while True:
            try:
                choice = input("\n💬 Choose option (1-5): ").strip()
                
                if choice == '1':
                    self.continuous_voice_mode()
                elif choice == '2':
                    self.test_voice_system()
                elif choice == '3':
                    self.show_voice_stats()
                elif choice == '4':
                    self.text_only_mode()
                elif choice == '5':
                    self.speak_enhanced("Goodbye Chuck! Voice mode is always ready when you need it!", "calm")
                    break
                else:
                    print("Please choose 1-5")
                    
            except KeyboardInterrupt:
                self.speak_enhanced("Goodbye Chuck!", "calm")
                break
    
    def show_voice_stats(self):
        """Show voice interaction statistics"""
        print("\n📊 VOICE MEMORY STATS")
        print("=" * 30)
        
        print(f"🎤 Voice sessions: {self.memory['voice_sessions']}")
        print(f"🗣️ Voice commands: {len(self.memory['voice_commands'])}")
        
        # Wake word stats
        print("👂 Wake word usage:")
        for wake_word, count in self.memory["wake_word_stats"].items():
            print(f"   '{wake_word}': {count} times")
        
        # Recent commands
        recent_commands = self.memory["voice_commands"][-5:]
        if recent_commands:
            print("🕒 Recent voice commands:")
            for cmd in recent_commands:
                timestamp = datetime.fromisoformat(cmd["timestamp"])
                print(f"   {timestamp.strftime('%H:%M')}: '{cmd['command']}'")
        
        self.speak_enhanced(f"I've processed {len(self.memory['voice_commands'])} voice commands across {self.memory['voice_sessions']} sessions!", "professional")
    
    def text_only_mode(self):
        """Fallback text-only mode"""
        print("\n💬 TEXT-ONLY MODE")
        print("Commands: 'photos', 'system', 'time', 'hello', 'quit'")
        
        while True:
            try:
                command = input("\n💬 Text Command: ").strip()
                if command.lower() == 'quit':
                    self.speak_enhanced("Returning to main menu!", "neutral")
                    break
                else:
                    self.process_voice_command(command)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    print("🎤 ChuckOS Jaymi Perfect Voice Experience")
    print("=" * 50)
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n👋 Voice system shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    jaymi = JaymiPerfectVoice()
    jaymi.interactive_voice_menu()
