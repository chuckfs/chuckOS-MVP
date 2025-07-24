#!/usr/bin/env python3
"""
Test real speech recognition for ChuckOS
"""

import speech_recognition as sr
import subprocess
import time

def test_microphone():
    """Test if microphone is working"""
    print("🎤 Testing microphone...")
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("✅ Microphone found!")
            print("🔧 Adjusting for ambient noise... (wait 2 seconds)")
            r.adjust_for_ambient_noise(source, duration=2)
            print("✅ Microphone calibrated!")
            return True
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return False

def listen_for_speech():
    """Listen for actual speech"""
    r = sr.Recognizer()
    
    print("\n🎧 SPEECH RECOGNITION TEST")
    print("=" * 40)
    print("Say something like:")
    print("- 'Hello Jaymi'")
    print("- 'Find my photos'") 
    print("- 'System status'")
    print("=" * 40)
    
    while True:
        try:
            with sr.Microphone() as source:
                print("\n🎤 Listening... (speak now)")
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
                
                print("🤔 Processing speech...")
                
                # Try Google Speech Recognition (free)
                try:
                    text = r.recognize_google(audio)
                    print(f"✅ You said: '{text}'")
                    
                    # Test response
                    response = f"I heard you say: {text}"
                    print(f"🤖 Jaymi: {response}")
                    subprocess.run(['espeak', '-s', '160', response], check=False)
                    
                    if 'quit' in text.lower() or 'exit' in text.lower():
                        print("👋 Goodbye!")
                        subprocess.run(['espeak', '-s', '160', 'Goodbye Chuck!'], check=False)
                        break
                        
                except sr.UnknownValueError:
                    print("❓ Couldn't understand that. Try speaking clearer.")
                except sr.RequestError as e:
                    print(f"❌ Speech service error: {e}")
                    print("💡 You might need internet connection for Google Speech Recognition")
                    
        except sr.WaitTimeoutError:
            print("⏰ No speech detected. Say something or press Ctrl+C to quit.")
        except KeyboardInterrupt:
            print("\n👋 Speech test ended!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 ChuckOS Speech Recognition Test")
    print("Week 2: Real Voice Input")
    
    if test_microphone():
        listen_for_speech()
    else:
        print("\n🔧 Microphone setup needed. In WSL, you might need:")
        print("- Install pulseaudio")
        print("- Configure WSL audio forwarding")
        print("- Use Windows microphone passthrough")
