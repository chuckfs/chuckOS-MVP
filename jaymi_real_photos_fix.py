#!/usr/bin/env python3
"""
Quick fix for Jaymi to find real photos instead of demo files
"""

import subprocess
import os
import sys
from pathlib import Path
import platform
import time
import random
from datetime import datetime

class JaymiRealPhotos:
    def __init__(self):
        self.name = "Jaymi"
        self.voice_active = True
        print("🤖 Jaymi Real Photos initialized - Looking for YOUR actual photos!")
    
    def speak(self, text, speed=160):
        """Make Jaymi speak"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', str(speed), '-p', '65', text], check=False)
            except:
                pass
        time.sleep(0.3)
    
    def find_real_photos(self):
        """Find real photos (ignore empty demo files)"""
        self.speak("Let me find your actual photos, not those demo files!")
        
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        real_files = []
        demo_files = []
        
        search_dirs = [
            Path.home() / "Pictures",
            Path.home() / "Downloads", 
            Path.home() / "Desktop",
            Path.home() / "Documents"  # Sometimes people save photos here
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for ext in extensions:
                    for file_path in search_dir.rglob(f"*{ext}"):
                        file_size = file_path.stat().st_size
                        
                        # Ignore empty files (demo files are 0 bytes)
                        if file_size > 0:
                            real_files.append(file_path)
                            print(f"   📸 Real photo found: {file_path.name} ({file_size/1024:.1f}KB)")
                        else:
                            demo_files.append(file_path)
                            print(f"   🎭 Demo file ignored: {file_path.name} (0KB)")
        
        if real_files:
            count = len(real_files)
            total_size = sum(f.stat().st_size for f in real_files)
            
            print(f"\n📸 Your Real Photo Collection:")
            print(f"   📊 Total: {count} real photos ({total_size/(1024*1024):.1f}MB)")
            
            # Show actual files with real info
            for i, photo in enumerate(real_files[:5], 1):
                size_mb = photo.stat().st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(photo.stat().st_mtime)
                print(f"   {i}. {photo.name} ({size_mb:.1f}MB, {mod_time.strftime('%b %d %Y')})")
            
            if count > 5:
                print(f"   ... and {count - 5} more real photos")
            
            self.speak(f"Perfect! I found {count} real photos totaling {total_size/(1024*1024):.1f} megabytes. These are your actual photos!")
            
        else:
            self.speak("I don't see any real photos yet - only those empty demo files I created earlier. Try adding some actual photos!")
            print("\n💡 To test with real photos:")
            print("   1. Copy some actual photos to ~/Pictures/")
            print("   2. Or take a screenshot with: gnome-screenshot -f ~/Pictures/screenshot.png")
            print("   3. Or download a test image: wget -O ~/Pictures/test.jpg https://picsum.photos/800/600")
            print("   4. Run this again to see Jaymi find your real photos!")
        
        if demo_files:
            print(f"\n🎭 Found {len(demo_files)} empty demo files to ignore")
        
        return real_files
    
    def clean_demo_files(self):
        """Clean up those fake demo files"""
        print("\n🧹 DEMO FILE CLEANUP")
        
        demo_files = []
        search_dirs = [Path.home() / "Pictures", Path.home() / "Documents"]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    for file_path in search_dir.rglob(f"*{ext}"):
                        if file_path.stat().st_size == 0:  # Empty files are demo files
                            demo_files.append(file_path)
        
        if demo_files:
            print(f"Found {len(demo_files)} empty demo files:")
            for f in demo_files:
                print(f"   🎭 {f.name} (0KB)")
            
            choice = input("\nDelete these fake demo files? (y/n): ").lower()
            if choice == 'y':
                for f in demo_files:
                    f.unlink()
                    print(f"   ✅ Deleted {f.name}")
                self.speak("Demo files cleaned up! Now I'll only find your real photos.")
                print("\n✅ All fake demo files removed!")
            else:
                print("Demo files kept. They'll be ignored when searching for real photos.")
        else:
            print("No demo files found to clean up.")
    
    def add_test_photo(self):
        """Download a test photo so we have something real to find"""
        print("\n📥 ADDING TEST PHOTO")
        self.speak("Let me download a test photo so I have something real to find!")
        
        try:
            # Download a test image
            subprocess.run([
                'wget', '-O', str(Path.home() / 'Pictures' / 'test_photo.jpg'),
                'https://picsum.photos/800/600'
            ], check=True)
            print("✅ Downloaded test_photo.jpg")
            self.speak("Perfect! I downloaded a test photo. Now let me find it!")
            return True
        except:
            print("❌ Couldn't download test photo. Try copying a real photo to ~/Pictures/")
            return False
    
    def interactive_mode(self):
        """Interactive mode for testing real photo finding"""
        print("\n🎤 REAL PHOTO FINDER MODE")
        print("Commands: 'photos', 'cleanup', 'add test photo', 'quit'")
        
        while True:
            try:
                command = input("\n💬 Command: ").strip().lower()
                
                if command == 'quit':
                    self.speak("Goodbye! I'm ready to find your real photos anytime.")
                    break
                elif command == 'photos' or 'photo' in command:
                    self.find_real_photos()
                elif command == 'cleanup':
                    self.clean_demo_files()
                elif 'test' in command or 'add' in command:
                    if self.add_test_photo():
                        time.sleep(1)
                        self.find_real_photos()
                else:
                    print("Commands: 'photos', 'cleanup', 'add test photo', 'quit'")
                    
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break

if __name__ == "__main__":
    print("🚀 Jaymi Real Photos - No More Demo Files!")
    print("=" * 50)
    
    jaymi = JaymiRealPhotos()
    jaymi.interactive_mode()
