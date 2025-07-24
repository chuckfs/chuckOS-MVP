#!/usr/bin/env python3
"""
Alternative speech using Windows Speech API
"""

import subprocess
import time

def simulate_voice_commands():
    """Simulate voice commands for development"""
    print("🎤 SIMULATED VOICE COMMANDS")
    print("(Since WSL microphone can be tricky)")
    print("=" * 40)
    
    commands = [
        "Hello Jaymi",
        "Find my photos", 
        "System status",
        "Open documents",
        "What time is it"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n{i}. Simulated: '{cmd}'")
        
        # Process the command (integrate with your existing logic)
        response = f"Processing voice command: {cmd}"
        print(f"🤖 Jaymi: {response}")
        subprocess.run(['espeak', '-s', '160', response], check=False)
        
        time.sleep(2)
    
    print("\n✅ Voice command simulation complete!")

if __name__ == "__main__":
    simulate_voice_commands()
