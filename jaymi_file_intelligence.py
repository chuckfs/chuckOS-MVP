#!/usr/bin/env python3
"""
ChuckOS Jaymi Advanced File Intelligence
Smart file organization, search, and management
"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
import mimetypes
import hashlib
import shutil
import re
from collections import defaultdict, Counter

class JaymiFileIntelligence:
    def __init__(self):
        self.name = "Jaymi File Intelligence"
        self.voice_active = True
        self.file_memory_file = Path.home() / ".jaymi_file_memory.json"
        
        # Load file intelligence memory
        self.file_memory = self.load_file_memory()
        
        # File categories
        self.file_categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf', '.odt'],
            'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'presentations': ['.ppt', '.pptx', '.odp'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.php', '.rb'],
            'data': ['.json', '.xml', '.yaml', '.sql', '.db', '.sqlite']
        }
        
        print("📁 Jaymi File Intelligence initialized")
        print(f"🧠 File patterns learned: {len(self.file_memory.get('file_patterns', {}))}")
    
    def load_file_memory(self):
        """Load file intelligence memory"""
        if self.file_memory_file.exists():
            try:
                with open(self.file_memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "file_patterns": {},
            "search_history": [],
            "organization_preferences": {},
            "file_associations": {},
            "smart_suggestions": [],
            "auto_organization_rules": []
        }
    
    def save_file_memory(self):
        """Save file intelligence memory"""
        try:
            with open(self.file_memory_file, 'w') as f:
                json.dump(self.file_memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Couldn't save file memory: {e}")
    
    def speak(self, text, speed=160):
        """Make Jaymi speak"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', str(speed), '-p', '65', text], check=False)
            except:
                pass
        time.sleep(0.2)
    
    def analyze_file_system(self):
        """Analyze the entire file system and learn patterns"""
        print("\n🔍 ANALYZING FILE SYSTEM...")
        print("=" * 40)
        
        self.speak("Let me analyze your file system and learn your organization patterns.")
        
        # Scan important directories
        scan_dirs = [
            Path.home() / "Documents",
            Path.home() / "Pictures", 
            Path.home() / "Downloads",
            Path.home() / "Desktop",
            Path.home() / "Music",
            Path.home() / "Videos"
        ]
        
        file_stats = defaultdict(int)
        size_stats = defaultdict(int)
        date_patterns = defaultdict(list)
        location_patterns = defaultdict(list)
        
        total_files = 0
        total_size = 0
        
        for scan_dir in scan_dirs:
            if scan_dir.exists():
                print(f"📂 Scanning {scan_dir.name}...")
                
                for file_path in scan_dir.rglob("*"):
                    if file_path.is_file():
                        try:
                            # Basic stats
                            file_size = file_path.stat().st_size
                            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            
                            # Skip empty files (probably demo files)
                            if file_size == 0:
                                continue
                            
                            total_files += 1
                            total_size += file_size
                            
                            # Categorize file
                            category = self.categorize_file(file_path)
                            file_stats[category] += 1
                            size_stats[category] += file_size
                            
                            # Learn date patterns
                            date_patterns[category].append(mod_time)
                            
                            # Learn location patterns
                            location_patterns[category].append(str(scan_dir.name))
                            
                        except (OSError, PermissionError):
                            continue
        
        # Analyze patterns
        print(f"\n📊 FILE SYSTEM ANALYSIS COMPLETE")
        print(f"   📁 Total files analyzed: {total_files}")
        print(f"   💾 Total size: {total_size / (1024*1024):.1f} MB")
        
        print(f"\n📂 File Categories:")
        for category, count in file_stats.items():
            if count > 0:
                avg_size = size_stats[category] / count / 1024  # KB
                print(f"   {category.title()}: {count} files (avg {avg_size:.1f}KB)")
        
        # Learn organization patterns
        self.learn_organization_patterns(location_patterns, date_patterns)
        
        # Generate smart suggestions
        suggestions = self.generate_smart_suggestions(file_stats, size_stats)
        
        self.speak(f"Analysis complete! I found {total_files} files and learned your organization patterns.")
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'categories': dict(file_stats),
            'suggestions': suggestions
        }
    
    def categorize_file(self, file_path):
        """Categorize a file based on extension and content"""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        
        return 'other'
    
    def learn_organization_patterns(self, location_patterns, date_patterns):
        """Learn how user organizes files"""
        print(f"\n🧠 LEARNING ORGANIZATION PATTERNS")
        
        # Analyze where different file types are stored
        for category, locations in location_patterns.items():
            if locations:
                most_common_location = Counter(locations).most_common(1)[0]
                
                self.file_memory["organization_preferences"][category] = {
                    "preferred_location": most_common_location[0],
                    "confidence": most_common_location[1] / len(locations),
                    "learned_on": datetime.now().isoformat()
                }
                
                print(f"   📂 {category.title()}: Usually stored in {most_common_location[0]}")
        
        # Analyze file creation/modification patterns
        for category, dates in date_patterns.items():
            if dates:
                # Find most active days/times
                hours = [d.hour for d in dates]
                most_active_hour = Counter(hours).most_common(1)[0][0] if hours else 12
                
                self.file_memory["file_patterns"][category] = {
                    "most_active_hour": most_active_hour,
                    "total_files": len(dates),
                    "learned_on": datetime.now().isoformat()
                }
        
        self.save_file_memory()
    
    def generate_smart_suggestions(self, file_stats, size_stats):
        """Generate intelligent file management suggestions"""
        suggestions = []
        
        # Storage optimization suggestions
        total_size_mb = sum(size_stats.values()) / (1024*1024)
        
        if total_size_mb > 1000:  # More than 1GB
            largest_category = max(size_stats.items(), key=lambda x: x[1])
            suggestions.append({
                "type": "storage_optimization",
                "message": f"Your {largest_category[0]} files are using {largest_category[1]/(1024*1024):.1f}MB. Consider archiving old files.",
                "priority": "medium"
            })
        
        # Organization suggestions
        downloads_files = file_stats.get('other', 0)
        if downloads_files > 20:
            suggestions.append({
                "type": "organization",
                "message": f"You have {downloads_files} uncategorized files. I can help organize them automatically.",
                "priority": "high"
            })
        
        # Cleanup suggestions
        if file_stats.get('archives', 0) > 5:
            suggestions.append({
                "type": "cleanup",
                "message": f"You have {file_stats['archives']} archive files. Some might be safe to remove after extraction.",
                "priority": "low"
            })
        
        # Store suggestions in memory
        self.file_memory["smart_suggestions"] = suggestions
        self.save_file_memory()
        
        return suggestions
    
    def smart_file_search(self, query):
        """Intelligent file search with natural language"""
        print(f"\n🔍 SMART SEARCH: '{query}'")
        print("=" * 40)
        
        self.speak(f"Searching for files matching '{query}' using intelligent algorithms.")
        
        # Remember this search
        self.file_memory["search_history"].append({
            "query": query,
            "timestamp": datetime.now().isoformat()
        })
        self.save_file_memory()
        
        query_lower = query.lower()
        found_files = []
        
        # Search directories
        search_dirs = [
            Path.home() / "Documents",
            Path.home() / "Pictures", 
            Path.home() / "Downloads",
            Path.home() / "Desktop",
            Path.home() / "Music",
            Path.home() / "Videos"
        ]
        
        # Different search strategies
        search_strategies = [
            self.search_by_filename,
            self.search_by_content_keywords,
            self.search_by_file_type,
            self.search_by_date_context,
            self.search_by_size_context
        ]
        
        for strategy in search_strategies:
            strategy_results = strategy(query_lower, search_dirs)
            found_files.extend(strategy_results)
        
        # Remove duplicates while preserving order
        unique_files = []
        seen = set()
        for file in found_files:
            if file not in seen:
                unique_files.append(file)
                seen.add(file)
        
        # Rank results by relevance
        ranked_files = self.rank_search_results(unique_files, query_lower)
        
        # Display results
        if ranked_files:
            print(f"📁 Found {len(ranked_files)} files:")
            
            for i, (file_path, score) in enumerate(ranked_files[:10], 1):
                size_mb = file_path.stat().st_size / (1024*1024)
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                category = self.categorize_file(file_path)
                
                print(f"   {i}. {file_path.name}")
                print(f"      📂 {file_path.parent}")
                print(f"      📊 {size_mb:.2f}MB • {category} • {mod_time.strftime('%b %d, %Y')}")
                print(f"      ⭐ Relevance: {score:.2f}")
                print()
            
            if len(ranked_files) > 10:
                print(f"   ... and {len(ranked_files) - 10} more files")
            
            self.speak(f"Found {len(ranked_files)} files matching your search. Showing the most relevant ones.")
        else:
            print("❌ No files found matching your search.")
            self.speak("I couldn't find any files matching that search. Try a different search term.")
        
        return ranked_files
    
    def search_by_filename(self, query, search_dirs):
        """Search by filename matching"""
        results = []
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for file_path in search_dir.rglob("*"):
                    if file_path.is_file() and file_path.stat().st_size > 0:
                        if query in file_path.name.lower():
                            results.append(file_path)
        
        return results
    
    def search_by_content_keywords(self, query, search_dirs):
        """Search by content keywords (for text files)"""
        results = []
        text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css', '.json']
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for file_path in search_dir.rglob("*"):
                    if (file_path.is_file() and 
                        file_path.suffix.lower() in text_extensions and
                        file_path.stat().st_size > 0 and
                        file_path.stat().st_size < 1024*1024):  # Max 1MB for text search
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read().lower()
                                if query in content:
                                    results.append(file_path)
                        except:
                            continue
        
        return results
    
    def search_by_file_type(self, query, search_dirs):
        """Search by file type keywords"""
        results = []
        
        # Map query keywords to file categories
        type_keywords = {
            'photo': 'images', 'picture': 'images', 'image': 'images',
            'document': 'documents', 'doc': 'documents', 'text': 'documents',
            'music': 'audio', 'song': 'audio', 'audio': 'audio',
            'video': 'video', 'movie': 'video',
            'code': 'code', 'script': 'code', 'program': 'code'
        }
        
        target_category = None
        for keyword, category in type_keywords.items():
            if keyword in query:
                target_category = category
                break
        
        if target_category:
            extensions = self.file_categories[target_category]
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for file_path in search_dir.rglob("*"):
                        if (file_path.is_file() and 
                            file_path.suffix.lower() in extensions and
                            file_path.stat().st_size > 0):
                            results.append(file_path)
        
        return results
    
    def search_by_date_context(self, query, search_dirs):
        """Search by date-related keywords"""
        results = []
        
        # Date keywords
        if any(word in query for word in ['today', 'recent', 'new', 'latest']):
            cutoff_date = datetime.now() - timedelta(days=7)  # Last week
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for file_path in search_dir.rglob("*"):
                        if file_path.is_file() and file_path.stat().st_size > 0:
                            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if mod_time > cutoff_date:
                                results.append(file_path)
        
        elif any(word in query for word in ['old', 'archive', 'backup']):
            cutoff_date = datetime.now() - timedelta(days=90)  # Older than 3 months
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for file_path in search_dir.rglob("*"):
                        if file_path.is_file() and file_path.stat().st_size > 0:
                            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if mod_time < cutoff_date:
                                results.append(file_path)
        
        return results
    
    def search_by_size_context(self, query, search_dirs):
        """Search by size-related keywords"""
        results = []
        
        if any(word in query for word in ['large', 'big', 'huge']):
            size_threshold = 10 * 1024 * 1024  # 10MB
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for file_path in search_dir.rglob("*"):
                        if (file_path.is_file() and 
                            file_path.stat().st_size > size_threshold):
                            results.append(file_path)
        
        elif any(word in query for word in ['small', 'tiny']):
            size_threshold = 100 * 1024  # 100KB
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    for file_path in search_dir.rglob("*"):
                        if (file_path.is_file() and 
                            0 < file_path.stat().st_size < size_threshold):
                            results.append(file_path)
        
        return results
    
    def rank_search_results(self, files, query):
        """Rank search results by relevance"""
        scored_files = []
        
        for file_path in files:
            score = 0.0
            filename_lower = file_path.name.lower()
            
            # Exact filename match gets highest score
            if query == filename_lower:
                score += 10.0
            
            # Filename contains query
            elif query in filename_lower:
                score += 5.0
            
            # Query words in filename
            query_words = query.split()
            for word in query_words:
                if word in filename_lower:
                    score += 2.0
            
            # Recent files get bonus
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            days_old = (datetime.now() - mod_time).days
            if days_old < 7:
                score += 1.0
            elif days_old < 30:
                score += 0.5
            
            # Preferred locations get bonus
            category = self.categorize_file(file_path)
            if category in self.file_memory.get("organization_preferences", {}):
                pref = self.file_memory["organization_preferences"][category]
                if pref["preferred_location"] in str(file_path.parent):
                    score += pref["confidence"]
            
            if score > 0:
                scored_files.append((file_path, score))
        
        # Sort by score (highest first)
        return sorted(scored_files, key=lambda x: x[1], reverse=True)
    
    def auto_organize_files(self):
        """Automatically organize files based on learned patterns"""
        print(f"\n🗂️ AUTO-ORGANIZING FILES")
        print("=" * 30)
        
        self.speak("Let me organize your files based on what I've learned about your preferences.")
        
        # Focus on Downloads folder (usually most disorganized)
        downloads_dir = Path.home() / "Downloads"
        
        if not downloads_dir.exists():
            print("❌ Downloads folder not found")
            return
        
        files_to_organize = []
        for file_path in downloads_dir.iterdir():
            if file_path.is_file() and file_path.stat().st_size > 0:
                files_to_organize.append(file_path)
        
        if not files_to_organize:
            print("✅ Downloads folder is already organized!")
            self.speak("Your downloads folder is already well organized!")
            return
        
        print(f"📁 Found {len(files_to_organize)} files to organize")
        
        organized_count = 0
        
        for file_path in files_to_organize:
            category = self.categorize_file(file_path)
            
            # Get preferred location for this category
            if category in self.file_memory.get("organization_preferences", {}):
                pref = self.file_memory["organization_preferences"][category]
                preferred_location = pref["preferred_location"]
                
                # Map location names to actual directories
                location_mapping = {
                    "Documents": Path.home() / "Documents",
                    "Pictures": Path.home() / "Pictures",
                    "Music": Path.home() / "Music",
                    "Videos": Path.home() / "Videos"
                }
                
                if preferred_location in location_mapping:
                    target_dir = location_mapping[preferred_location]
                    
                    try:
                        # Ensure target directory exists
                        target_dir.mkdir(exist_ok=True)
                        
                        # Move file
                        target_path = target_dir / file_path.name
                        
                        # Handle naming conflicts
                        counter = 1
                        while target_path.exists():
                            stem = file_path.stem
                            suffix = file_path.suffix
                            target_path = target_dir / f"{stem}_{counter}{suffix}"
                            counter += 1
                        
                        shutil.move(str(file_path), str(target_path))
                        print(f"   📁 Moved {file_path.name} to {preferred_location}")
                        organized_count += 1
                        
                    except Exception as e:
                        print(f"   ❌ Couldn't move {file_path.name}: {e}")
        
        print(f"\n✅ Organized {organized_count} files based on learned patterns!")
        self.speak(f"Successfully organized {organized_count} files into their preferred locations!")
        
        return organized_count
    
    def show_file_insights(self):
        """Show intelligent insights about file system"""
        print(f"\n💡 FILE SYSTEM INSIGHTS")
        print("=" * 30)
        
        # Show learned patterns
        if self.file_memory.get("organization_preferences"):
            print("🗂️ Organization Patterns:")
            for category, pref in self.file_memory["organization_preferences"].items():
                confidence_pct = pref["confidence"] * 100
                print(f"   {category.title()}: {pref['preferred_location']} ({confidence_pct:.1f}% confidence)")
        
        # Show smart suggestions
        if self.file_memory.get("smart_suggestions"):
            print(f"\n💡 Smart Suggestions:")
            for suggestion in self.file_memory["smart_suggestions"][:3]:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[suggestion["priority"]]
                print(f"   {priority_emoji} {suggestion['message']}")
        
        # Show search history
        if self.file_memory.get("search_history"):
            recent_searches = self.file_memory["search_history"][-5:]
            print(f"\n🔍 Recent Searches:")
            for search in recent_searches:
                timestamp = datetime.fromisoformat(search["timestamp"])
                print(f"   '{search['query']}' ({timestamp.strftime('%b %d, %H:%M')})")
        
        self.speak("Here are the intelligent insights I've gathered about your file system.")
    
    def interactive_file_intelligence(self):
        """Interactive file intelligence interface"""
        print(f"\n📁 JAYMI FILE INTELLIGENCE")
        print("=" * 50)
        print("Commands:")
        print("  'analyze' - Analyze entire file system")
        print("  'search [query]' - Smart file search")
        print("  'organize' - Auto-organize files")
        print("  'insights' - Show file system insights")
        print("  'suggestions' - Show smart suggestions")
        print("  'quit' - Exit")
        
        while True:
            try:
                command = input("\n💬 File Command: ").strip().lower()
                
                if command == 'quit':
                    self.speak("File intelligence session complete! I'll remember everything I learned.")
                    break
                    
                elif command == 'analyze':
                    self.analyze_file_system()
                    
                elif command.startswith('search '):
                    query = command[7:]  # Remove 'search '
                    if query:
                        self.smart_file_search(query)
                    else:
                        print("Please provide a search query")
                        
                elif command == 'organize':
                    self.auto_organize_files()
                    
                elif command == 'insights':
                    self.show_file_insights()
                    
                elif command == 'suggestions':
                    if self.file_memory.get("smart_suggestions"):
                        print("💡 Smart Suggestions:")
                        for i, suggestion in enumerate(self.file_memory["smart_suggestions"], 1):
                            print(f"{i}. {suggestion['message']} ({suggestion['priority']} priority)")
                        self.speak(f"I have {len(self.file_memory['smart_suggestions'])} smart suggestions for you.")
                    else:
                        print("No suggestions yet. Run 'analyze' first!")
                        self.speak("I need to analyze your files first to provide suggestions.")
                
                else:
                    print("Unknown command. Try 'analyze', 'search [query]', 'organize', 'insights', or 'quit'")
                    
            except KeyboardInterrupt:
                self.speak("File intelligence session ended!")
                break

if __name__ == "__main__":
    print("📁 ChuckOS Jaymi Advanced File Intelligence")
    print("=" * 50)
    
    jaymi = JaymiFileIntelligence()
    jaymi.interactive_file_intelligence()
