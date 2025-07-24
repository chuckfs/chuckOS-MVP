#!/usr/bin/env python3
"""
ChuckOS Jaymi Smart Memory System
Makes Jaymi remember preferences and learn from interactions
"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class JaymiSmartMemory:
    def __init__(self):
        self.name = "Jaymi Smart"
        self.voice_active = True
        self.memory_file = Path.home() / ".jaymi_memory.json"
        self.session_file = Path.home() / ".jaymi_session.json"
        
        # Load existing memory
        self.memory = self.load_memory()
        self.session_data = self.load_session()
        
        print("🧠 Jaymi Smart Memory initialized")
        print(f"📚 Loaded {len(self.memory.get('interactions', []))} past interactions")
        print(f"🎯 Session #{self.session_data['session_count']}")
    
    def speak(self, text, speed=160):
        """Make Jaymi speak with memory-enhanced responses"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', str(speed), '-p', '65', text], check=False)
            except:
                pass
        time.sleep(0.3)
        
        # Remember what Jaymi said
        self.remember_interaction("jaymi_response", text)
    
    def load_memory(self):
        """Load Jaymi's memory from file"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default memory structure
        return {
            "user_preferences": {},
            "interactions": [],
            "learned_patterns": {},
            "favorite_commands": defaultdict(int),
            "user_info": {},
            "daily_routines": {}
        }
    
    def load_session(self):
        """Load current session data"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    # Start new session
                    data['session_count'] += 1
                    data['session_start'] = datetime.now().isoformat()
                    self.save_session(data)
                    return data
            except:
                pass
        
        # First session
        data = {
            "session_count": 1,
            "session_start": datetime.now().isoformat(),
            "total_interactions": 0,
            "favorite_time": None
        }
        self.save_session(data)
        return data
    
    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Couldn't save memory: {e}")
    
    def save_session(self, data=None):
        """Save session data"""
        if data is None:
            data = self.session_data
        try:
            with open(self.session_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Couldn't save session: {e}")
    
    def remember_interaction(self, interaction_type, content, metadata=None):
        """Remember an interaction"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,
            "content": content,
            "session": self.session_data['session_count']
        }
        
        if metadata:
            interaction["metadata"] = metadata
        
        self.memory["interactions"].append(interaction)
        
        # Keep only last 1000 interactions to prevent file bloat
        if len(self.memory["interactions"]) > 1000:
            self.memory["interactions"] = self.memory["interactions"][-1000:]
        
        self.save_memory()
    
    def learn_preference(self, category, key, value):
        """Learn a user preference"""
        if category not in self.memory["user_preferences"]:
            self.memory["user_preferences"][category] = {}
        
        self.memory["user_preferences"][category][key] = {
            "value": value,
            "learned_on": datetime.now().isoformat(),
            "confidence": 1.0
        }
        self.save_memory()
        print(f"🧠 Learned: {category}.{key} = {value}")
    
    def get_preference(self, category, key, default=None):
        """Get a learned preference"""
        try:
            return self.memory["user_preferences"][category][key]["value"]
        except KeyError:
            return default
    
    def smart_greeting(self):
        """Smart greeting based on memory and patterns"""
        now = datetime.now()
        hour = now.hour
        
        # Analyze past interaction times
        recent_interactions = [
            i for i in self.memory["interactions"] 
            if (datetime.now() - datetime.fromisoformat(i["timestamp"])).days < 7
        ]
        
        if recent_interactions:
            avg_hour = sum(
                datetime.fromisoformat(i["timestamp"]).hour 
                for i in recent_interactions
            ) / len(recent_interactions)
            
            if abs(hour - avg_hour) < 2:
                time_pattern = "right on schedule"
            elif hour < avg_hour - 2:
                time_pattern = "earlier than usual"
            else:
                time_pattern = "later than usual"
        else:
            time_pattern = "at a new time"
        
        # Check last interaction
        if self.memory["interactions"]:
            last_interaction = datetime.fromisoformat(self.memory["interactions"][-1]["timestamp"])
            time_since = datetime.now() - last_interaction
            
            if time_since.days > 7:
                duration_msg = "It's been over a week! I missed you."
            elif time_since.days > 1:
                duration_msg = f"It's been {time_since.days} days since we last talked."
            elif time_since.seconds > 3600:
                hours = time_since.seconds // 3600
                duration_msg = f"It's been {hours} hours since our last session."
            else:
                duration_msg = "Welcome back!"
        else:
            duration_msg = "Nice to meet you for the first time!"
        
        # Time-based greeting
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Working late tonight?"
        
        greeting = f"{time_greeting}, Chuck! {duration_msg} You're here {time_pattern}."
        
        # Add personalized touch based on preferences
        if self.get_preference("interaction", "formality") == "casual":
            greeting = greeting.replace("Chuck", "buddy")
        
        self.speak(greeting)
        
        # Remember this greeting pattern
        self.remember_interaction("greeting", greeting, {
            "hour": hour,
            "time_pattern": time_pattern,
            "session_number": self.session_data['session_count']
        })
    
    def smart_photo_search(self):
        """Enhanced photo search with learning"""
        self.speak("Let me find your photos and remember what you're looking for.")
        
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
                        if file_path.stat().st_size > 0:  # Only real files
                            found_files.append(file_path)
        
        if found_files:
            # Learn about photo preferences
            total_size = sum(f.stat().st_size for f in found_files)
            avg_size = total_size / len(found_files)
            
            # Categorize by size (learn user's photo types)
            large_photos = [f for f in found_files if f.stat().st_size > avg_size * 2]
            recent_photos = sorted(found_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            
            # Smart response based on learned patterns
            prev_searches = [
                i for i in self.memory["interactions"] 
                if i["type"] == "photo_search"
            ]
            
            if len(prev_searches) > 2:
                self.speak(f"I found {len(found_files)} photos. Based on your previous searches, you usually look at the most recent ones first.")
                preference = "recent_first"
            else:
                self.speak(f"I found {len(found_files)} photos. I'm learning your preferences - would you like to see recent ones or all of them?")
                preference = "learning"
            
            # Display results intelligently
            print(f"📸 Smart Photo Analysis:")
            print(f"   📊 Total: {len(found_files)} photos ({total_size/(1024*1024):.1f}MB)")
            
            if large_photos:
                print(f"   📷 High-res photos: {len(large_photos)}")
            
            print(f"   🕒 Most recent:")
            for i, photo in enumerate(recent_photos[:3], 1):
                mod_time = datetime.fromtimestamp(photo.stat().st_mtime)
                print(f"     {i}. {photo.name} ({mod_time.strftime('%b %d')})")
            
            # Remember this search
            self.remember_interaction("photo_search", f"Found {len(found_files)} photos", {
                "count": len(found_files),
                "total_size": total_size,
                "preference_shown": preference
            })
            
            # Learn user's photo habits
            self.learn_preference("photos", "average_collection_size", len(found_files))
            
            return found_files
        else:
            self.speak("No photos found yet. When you add some, I'll remember your preferences!")
            return []
    
    def analyze_user_patterns(self):
        """Analyze and report learned patterns"""
        print("\n🧠 SMART MEMORY ANALYSIS")
        print("=" * 40)
        
        # Session patterns
        interactions_by_hour = defaultdict(int)
        for interaction in self.memory["interactions"]:
            hour = datetime.fromisoformat(interaction["timestamp"]).hour
            interactions_by_hour[hour] += 1
        
        if interactions_by_hour:
            most_active_hour = max(interactions_by_hour, key=interactions_by_hour.get)
            print(f"🕒 Most active time: {most_active_hour}:00")
            
            # Learn this pattern
            self.learn_preference("schedule", "preferred_hour", most_active_hour)
        
        # Command preferences
        command_types = defaultdict(int)
        for interaction in self.memory["interactions"]:
            if interaction["type"] == "user_command":
                command_types[interaction["content"].split()[0]] += 1
        
        if command_types:
            favorite_command = max(command_types, key=command_types.get)
            print(f"💻 Favorite command: '{favorite_command}' (used {command_types[favorite_command]} times)")
            
            # Learn this preference
            self.learn_preference("commands", "most_used", favorite_command)
        
        # Preferences summary
        print(f"📚 Total learned preferences: {sum(len(cat) for cat in self.memory['user_preferences'].values())}")
        print(f"🗣️ Total interactions remembered: {len(self.memory['interactions'])}")
        print(f"📊 Current session: #{self.session_data['session_count']}")
        
        self.speak(f"I've learned {sum(len(cat) for cat in self.memory['user_preferences'].values())} things about your preferences across {self.session_data['session_count']} sessions!")
    
    def interactive_smart_mode(self):
        """Interactive mode with smart memory"""
        self.smart_greeting()
        
        print("\n🧠 JAYMI SMART MEMORY MODE")
        print("Commands: 'photos', 'patterns', 'memory', 'preferences', 'quit'")
        
        while True:
            try:
                command = input("\n💬 Command: ").strip().lower()
                
                # Remember user command
                self.remember_interaction("user_command", command)
                
                if command == 'quit':
                    # Smart goodbye
                    session_length = datetime.now() - datetime.fromisoformat(self.session_data['session_start'])
                    
                    if session_length.seconds < 300:  # Less than 5 minutes
                        goodbye = "That was a quick session! See you soon, Chuck!"
                    elif session_length.seconds > 3600:  # More than 1 hour
                        goodbye = "Wow, we've been chatting for a while! Thanks for spending time with me."
                    else:
                        goodbye = "Great session, Chuck! I learned more about your preferences."
                    
                    self.speak(goodbye)
                    self.remember_interaction("session_end", goodbye)
                    break
                    
                elif command == 'photos' or 'photo' in command:
                    self.smart_photo_search()
                    
                elif command == 'patterns':
                    self.analyze_user_patterns()
                    
                elif command == 'memory':
                    recent_count = len([
                        i for i in self.memory["interactions"] 
                        if (datetime.now() - datetime.fromisoformat(i["timestamp"])).days < 7
                    ])
                    self.speak(f"I remember {len(self.memory['interactions'])} total interactions, with {recent_count} from this week.")
                    
                elif command == 'preferences':
                    prefs = self.memory["user_preferences"]
                    if prefs:
                        print("🎯 Learned Preferences:")
                        for category, items in prefs.items():
                            print(f"   {category.title()}:")
                            for key, data in items.items():
                                print(f"     • {key}: {data['value']}")
                        self.speak(f"I've learned preferences in {len(prefs)} categories.")
                    else:
                        self.speak("I'm still learning your preferences. Keep using me and I'll get smarter!")
                        
                else:
                    # Smart response based on past interactions
                    similar_commands = [
                        i for i in self.memory["interactions"] 
                        if i["type"] == "user_command" and command in i["content"]
                    ]
                    
                    if similar_commands:
                        self.speak(f"I remember you asking about '{command}' before. I'm getting better at understanding you!")
                    else:
                        self.speak(f"New command '{command}'! I'm learning something new about what you like to do.")
                    
                    # Remember this as a learning opportunity
                    self.remember_interaction("unknown_command", command)
                    
            except KeyboardInterrupt:
                self.speak("Goodbye! I'll remember our conversation for next time.")
                break

if __name__ == "__main__":
    print("🧠 ChuckOS Jaymi Smart Memory System")
    print("=" * 50)
    
    jaymi = JaymiSmartMemory()
    jaymi.interactive_smart_mode()
