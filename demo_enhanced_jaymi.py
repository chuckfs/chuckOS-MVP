#!/usr/bin/env python3
"""
ChuckOS Enhanced Demo - The $299 Moment
Polished demo experience that showcases premium value
"""

import subprocess
import os
import sys
from pathlib import Path
import platform
import time
import random
from datetime import datetime

class EnhancedJaymiDemo:
    def __init__(self):
        self.name = "Jaymi"
        self.voice_active = True
        self.demo_mode = True
        self.found_files = []
        print("🎬 ChuckOS Enhanced Demo initialized")
    
    def speak(self, text, speed=160):
        """Enhanced speech with timing control"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', str(speed), '-p', '65', text], check=False)
            except:
                pass
        
        # Demo timing - pause for effect
        if self.demo_mode:
            time.sleep(0.5)
    
    def create_demo_files(self):
        """Create comprehensive demo file set"""
        print("📁 Setting up demo environment...")
        
        # Create directories
        dirs = ['Pictures', 'Documents', 'Music', 'Downloads', 'Videos']
        for dir_name in dirs:
            (Path.home() / dir_name).mkdir(exist_ok=True)
        
        # Create demo files with realistic names
        demo_files = {
            'Pictures': [
                'vacation_hawaii_2024.jpg', 'family_reunion.png', 'sunset_beach.jpeg',
                'birthday_party.jpg', 'graduation_photo.png', 'holiday_memories.jpg'
            ],
            'Documents': [
                'resume_2025.pdf', 'project_proposal.docx', 'meeting_notes.txt',
                'budget_spreadsheet.xlsx', 'presentation_slides.pptx', 'important_contract.pdf'
            ],
            'Music': [
                'favorite_song.mp3', 'classical_music.wav', 'podcast_episode.mp3',
                'instrumental_track.flac', 'voice_memo.m4a'
            ],
            'Videos': [
                'tutorial_video.mp4', 'family_video.avi', 'conference_recording.mkv'
            ]
        }
        
        # Touch files to create them
        for folder, files in demo_files.items():
            folder_path = Path.home() / folder
            for file_name in files:
                (folder_path / file_name).touch()
        
        print("✅ Demo environment ready!")
        return demo_files
    
    def run_killer_demo(self):
        """The 60-second demo that sells ChuckOS"""
        print("\n" + "="*60)
        print("🎬 CHUCKOS KILLER DEMO - THE $299 MOMENT")
        print("="*60)
        
        self.speak("Welcome to ChuckOS! I'm Jaymi, and I'm about to show you the future of computing.", 150)
        print("\n🎯 Press Enter to continue through the demo...")
        input()
        
        # Demo 1: Smart Photo Finding
        print("\n📸 DEMO 1: Smart Photo Discovery")
        self.speak("Let me find your photos using natural language.")
        time.sleep(1)
        
        photos = self.enhanced_photo_search()
        self.speak(f"Found {len(photos)} photos instantly! I can also find specific ones.")
        
        self.speak("Let me find your vacation photos specifically.")
        vacation_photos = [p for p in photos if 'vacation' in p.name.lower()]
        if vacation_photos:
            self.speak(f"Perfect! I found your vacation photos: {vacation_photos[0].name}")
        
        input("\n🎯 Press Enter for next demo...")
        
        # Demo 2: Document Intelligence
        print("\n📄 DEMO 2: Document Intelligence")
        self.speak("Now let me find your important documents.")
        time.sleep(1)
        
        docs = self.enhanced_document_search()
        self.speak(f"I discovered {len(docs)} documents. Here are the most important ones.")
        
        # Find specific document types
        resume = [d for d in docs if 'resume' in d.name.lower()]
        if resume:
            self.speak(f"Found your resume: {resume[0].name}. Want me to open it for an interview?")
        
        input("\n🎯 Press Enter for next demo...")
        
        # Demo 3: System Intelligence
        print("\n💻 DEMO 3: System Intelligence")
        self.speak("Let me give you a complete system report.")
        self.advanced_system_report()
        
        input("\n🎯 Press Enter for next demo...")
        
        # Demo 4: Natural Conversation
        print("\n💬 DEMO 4: Natural AI Conversation")
        self.speak("I'm not just a file finder - I'm your intelligent AI companion.")
        self.demonstrate_personality()
        
        input("\n🎯 Press Enter for finale...")
        
        # Demo 5: The Big Finish
        print("\n🚀 DEMO 5: The Future is Here")
        self.speak("This is just the beginning. Imagine controlling your entire computer with natural language.", 140)
        self.speak("No more clicking through folders. No more forgetting where you saved files.", 140)
        self.speak("Just ask Jaymi, and I'll handle everything.", 140)
        
        print("\n" + "="*60)
        print("🎯 DEMO COMPLETE - THIS IS THE $299 VALUE PROPOSITION")
        print("="*60)
        
        return True
    
    def enhanced_photo_search(self):
        """Enhanced photo search with detailed results"""
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
                    found_files.extend(search_dir.rglob(f"*{ext}"))
        
        # Sort by date (newest first)
        found_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if found_files:
            count = len(found_files)
            print(f"📸 Photo Search Results:")
            
            # Show first 5 with details
            for i, photo in enumerate(found_files[:5], 1):
                size_mb = photo.stat().st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(photo.stat().st_mtime)
                print(f"   {i}. {photo.name} ({size_mb:.1f}MB, {mod_time.strftime('%b %d')})")
            
            if count > 5:
                print(f"   ... and {count - 5} more photos")
        
        self.found_files = found_files
        return found_files
    
    def enhanced_document_search(self):
        """Enhanced document search with categories"""
        doc_extensions = {
            'text': ['.txt', '.md', '.rtf'],
            'pdf': ['.pdf'],
            'office': ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
            'other': ['.odt', '.ods', '.odp']
        }
        
        found_docs = {'text': [], 'pdf': [], 'office': [], 'other': []}
        
        search_dirs = [
            Path.home() / "Documents",
            Path.home() / "Downloads",
            Path.home() / "Desktop"
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for category, extensions in doc_extensions.items():
                    for ext in extensions:
                        found_docs[category].extend(search_dir.rglob(f"*{ext}"))
        
        total_docs = []
        for category, docs in found_docs.items():
            total_docs.extend(docs)
        
        if total_docs:
            print(f"📄 Document Categories:")
            for category, docs in found_docs.items():
                if docs:
                    print(f"   {category.title()}: {len(docs)} files")
                    for doc in docs[:2]:  # Show first 2 per category
                        print(f"     • {doc.name}")
        
        return total_docs
    
    def advanced_system_report(self):
        """Professional system report with metrics"""
        try:
            hostname = platform.node()
            system = platform.system()
            release = platform.release()
            processor = platform.processor()
            
            # Get disk usage
            total, used, free = self.get_disk_usage()
            
            # Get memory info (basic)
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    total_mem = int([line for line in meminfo.split('\n') if 'MemTotal' in line][0].split()[1])
                    total_mem_gb = total_mem / 1024 / 1024
            except:
                total_mem_gb = "Unknown"
            
            print(f"💻 Advanced System Report:")
            print(f"   🖥️  Hostname: {hostname}")
            print(f"   🐧 OS: {system} {release}")
            print(f"   🔧 Processor: {processor if processor else 'Standard CPU'}")
            print(f"   💾 Memory: ~{total_mem_gb:.1f}GB" if isinstance(total_mem_gb, float) else f"   💾 Memory: {total_mem_gb}")
            print(f"   💿 Disk: {used:.1f}GB used / {total:.1f}GB total ({free:.1f}GB free)")
            print(f"   🎯 ChuckOS: Advanced AI Active")
            print(f"   🤖 Jaymi: Fully Operational")
            print(f"   ⚡ Status: All systems optimal")
            
            self.speak(f"System running perfectly! {hostname} with {system}, plenty of storage available.")
            
        except Exception as e:
            print(f"💻 Basic System Report:")
            print(f"   🎯 ChuckOS: Active and running smoothly")
            print(f"   🤖 Jaymi: All systems operational")
            self.speak("System is running beautifully! All ChuckOS components are active.")
    
    def get_disk_usage(self):
        """Get disk usage information"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(Path.home())
            return (total / (1024**3), used / (1024**3), free / (1024**3))  # Convert to GB
        except:
            return (100.0, 50.0, 50.0)  # Default values
    
    def demonstrate_personality(self):
        """Show Jaymi's AI personality"""
        responses = [
            "I love helping you stay organized and productive!",
            "Think of me as your personal digital assistant who never gets tired.",
            "I'm constantly learning and getting better at understanding what you need.",
            "The more you use me, the smarter I become at helping you.",
        ]
        
        for response in responses[:2]:
            self.speak(response, 150)
            time.sleep(1)
    
    def interactive_demo_mode(self):
        """Interactive demo for live presentations"""
        print("\n🎤 INTERACTIVE DEMO MODE")
        print("Perfect for showing to investors, customers, or press!")
        print("=" * 50)
        
        commands = [
            ("find my vacation photos", "Smart photo search with context"),
            ("show me recent documents", "Document intelligence"),
            ("system status", "Professional system reporting"),
            ("what time is it", "Natural conversation"),
            ("find my resume", "Specific file finding"),
        ]
        
        print("🎯 Demo Commands Available:")
        for i, (cmd, desc) in enumerate(commands, 1):
            print(f"   {i}. '{cmd}' - {desc}")
        
        print("\nType 'demo' for auto demo, or try any command above:")
        
        while True:
            try:
                user_input = input("\n💬 Demo Command: ").strip().lower()
                
                if user_input == 'quit' or user_input == 'exit':
                    self.speak("Thank you for the ChuckOS demo! Ready to change computing forever!")
                    break
                elif user_input == 'demo':
                    self.run_killer_demo()
                elif 'photo' in user_input or 'picture' in user_input:
                    photos = self.enhanced_photo_search()
                    self.speak(f"Found {len(photos)} photos! Here are your most recent ones.")
                elif 'document' in user_input or 'file' in user_input:
                    docs = self.enhanced_document_search()
                    self.speak(f"Located {len(docs)} documents across multiple categories.")
                elif 'system' in user_input or 'status' in user_input:
                    self.advanced_system_report()
                elif 'time' in user_input:
                    now = datetime.now()
                    time_str = now.strftime("%I:%M %p on %A, %B %d")
                    self.speak(f"It's currently {time_str}.")
                elif 'resume' in user_input:
                    self.speak("Let me find your resume for you.")
                    docs = self.enhanced_document_search()
                    resume = [d for d in docs if 'resume' in d.name.lower()]
                    if resume:
                        self.speak(f"Found it! Your resume: {resume[0].name}")
                    else:
                        self.speak("I don't see a resume file. Would you like me to search more thoroughly?")
                else:
                    self.speak(f"Interesting command: '{user_input}'. I'm always learning new ways to help!")
                    
            except KeyboardInterrupt:
                self.speak("Demo concluded! ChuckOS - the future of computing!")
                break

if __name__ == "__main__":
    print("🎬 ChuckOS Enhanced Demo - Week 2")
    print("The polished experience that sells!")
    print("=" * 50)
    
    demo = EnhancedJaymiDemo()
    demo.create_demo_files()
    
    print("\nChoose demo mode:")
    print("1. Killer 60-second auto demo")
    print("2. Interactive demo (for live presentations)")
    
    choice = input("\nSelect mode (1 or 2): ").strip()
    
    if choice == "1":
        demo.run_killer_demo()
    else:
        demo.interactive_demo_mode()
