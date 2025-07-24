#!/usr/bin/env python3
"""
Jaymi File Intelligence API
Extracted and adapted from the original JaymiFileIntelligence for web service use
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
import mimetypes
import hashlib
import asyncio
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Any
import tempfile

class JaymiFileIntelligenceAPI:
    """
    Web API version of Jaymi File Intelligence
    Adapted from the original CLI version for SaaS use
    """
    
    def __init__(self):
        self.name = "Jaymi File Intelligence API"
        
        # File categories (extracted from original)
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
    
    async def smart_search(self, query: str, user_id: int, file_paths: List[str] = None) -> Dict[str, Any]:
        """
        Smart file search with natural language (async version)
        Extracted from original smart_file_search method
        """
        start_time = time.time()
        
        query_lower = query.lower()
        found_files = []
        
        # Default search directories if none provided
        if not file_paths:
            search_dirs = [
                Path.home() / "Documents",
                Path.home() / "Pictures", 
                Path.home() / "Downloads",
                Path.home() / "Desktop",
                Path.home() / "Music",
                Path.home() / "Videos"
            ]
        else:
            search_dirs = [Path(p) for p in file_paths]
        
        # Search strategies (extracted from original)
        strategies = [
            self._search_by_filename,
            self._search_by_content_keywords,
            self._search_by_file_type,
            self._search_by_date_context,
            self._search_by_size_context
        ]
        
        for strategy in strategies:
            strategy_results = await strategy(query_lower, search_dirs)
            found_files.extend(strategy_results)
        
        # Remove duplicates
        unique_files = []
        seen = set()
        for file in found_files:
            file_str = str(file)
            if file_str not in seen:
                unique_files.append(file)
                seen.add(file_str)
        
        # Rank results (extracted from original)
        ranked_files = self._rank_search_results(unique_files, query_lower, user_id)
        
        search_time = time.time() - start_time
        
        # Format results for API response
        results = []
        for file_path, score in ranked_files[:20]:  # Limit to 20 results
            try:
                stat = file_path.stat()
                results.append({
                    "filename": file_path.name,
                    "path": str(file_path.parent),
                    "full_path": str(file_path),
                    "size": stat.st_size,
                    "size_mb": round(stat.st_size / (1024*1024), 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "category": self._categorize_file(file_path),
                    "relevance_score": round(score, 2)
                })
            except (OSError, PermissionError):
                continue
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results),
            "search_time": round(search_time, 3)
        }
    
    async def analyze_file(self, file_path: str, original_name: str, user_id: int) -> Dict[str, Any]:
        """
        Analyze a single uploaded file
        """
        path = Path(file_path)
        
        try:
            stat = path.stat()
            category = self._categorize_file(path)
            
            analysis = {
                "filename": original_name,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024*1024), 2),
                "category": category,
                "extension": path.suffix.lower(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            }
            
            # Add content analysis for text files
            if category == 'documents' and stat.st_size < 1024*1024:  # Max 1MB
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        analysis["word_count"] = len(content.split())
                        analysis["line_count"] = len(content.splitlines())
                except:
                    pass
            
            return analysis
            
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_system(self, user_id: int) -> Dict[str, Any]:
        """
        Analyze file system and generate insights (async version)
        Extracted from original analyze_file_system method
        """
        # Default scan directories
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
                async for file_path in self._async_scan_directory(scan_dir):
                    if file_path.is_file():
                        try:
                            stat = file_path.stat()
                            file_size = stat.st_size
                            mod_time = datetime.fromtimestamp(stat.st_mtime)
                            
                            # Skip empty files
                            if file_size == 0:
                                continue
                            
                            total_files += 1
                            total_size += file_size
                            
                            # Categorize file
                            category = self._categorize_file(file_path)
                            file_stats[category] += 1
                            size_stats[category] += file_size
                            
                            # Learn patterns
                            date_patterns[category].append(mod_time)
                            location_patterns[category].append(str(scan_dir.name))
                            
                        except (OSError, PermissionError):
                            continue
        
        # Generate insights
        suggestions = self._generate_suggestions(file_stats, size_stats)
        
        return {
            "total_files": total_files,
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024*1024), 2),
            "categories": dict(file_stats),
            "category_sizes": {k: round(v / (1024*1024), 2) for k, v in size_stats.items()},
            "suggestions": suggestions,
            "analyzed_at": datetime.now().isoformat()
        }
    
    async def analyze_path(self, path: str, user_id: int) -> Dict[str, Any]:
        """
        Analyze a specific path
        """
        target_path = Path(path)
        
        if not target_path.exists():
            raise ValueError(f"Path does not exist: {path}")
        
        if target_path.is_file():
            return await self.analyze_file(str(target_path), target_path.name, user_id)
        
        # Directory analysis
        file_stats = defaultdict(int)
        size_stats = defaultdict(int)
        total_files = 0
        total_size = 0
        
        async for file_path in self._async_scan_directory(target_path):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    file_size = stat.st_size
                    
                    if file_size == 0:
                        continue
                    
                    total_files += 1
                    total_size += file_size
                    
                    category = self._categorize_file(file_path)
                    file_stats[category] += 1
                    size_stats[category] += file_size
                    
                except (OSError, PermissionError):
                    continue
        
        return {
            "path": str(target_path),
            "total_files": total_files,
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024*1024), 2),
            "categories": dict(file_stats),
            "category_sizes": {k: round(v / (1024*1024), 2) for k, v in size_stats.items()}
        }
    
    async def get_insights(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get AI-generated insights about user's file organization
        """
        # This would integrate with user's stored patterns and history
        # For now, providing general insights
        insights = [
            {
                "type": "organization",
                "title": "File Organization Patterns",
                "message": "I've learned your file organization preferences and can help maintain consistency.",
                "priority": "medium"
            },
            {
                "type": "storage",
                "title": "Storage Optimization",
                "message": "Regular cleanup of temporary files can free up valuable storage space.",
                "priority": "low"
            },
            {
                "type": "productivity",
                "title": "Search Efficiency",
                "message": "Using natural language search queries gets better results than exact filename matching.",
                "priority": "high"
            }
        ]
        
        return insights
    
    async def auto_organize(self, path: Optional[str], user_id: int, dry_run: bool = True) -> Dict[str, Any]:
        """
        Auto-organize files based on learned patterns
        """
        target_path = Path(path) if path else Path.home() / "Downloads"
        
        if not target_path.exists():
            raise ValueError(f"Path does not exist: {target_path}")
        
        files_to_organize = []
        for file_path in target_path.iterdir():
            if file_path.is_file() and file_path.stat().st_size > 0:
                files_to_organize.append(file_path)
        
        organization_plan = []
        
        for file_path in files_to_organize:
            category = self._categorize_file(file_path)
            
            # Simple organization rules (could be enhanced with learned patterns)
            target_dir = self._get_target_directory(category)
            
            if target_dir and target_dir != file_path.parent:
                organization_plan.append({
                    "file": file_path.name,
                    "from": str(file_path.parent),
                    "to": str(target_dir),
                    "category": category,
                    "action": "move"
                })
        
        if not dry_run:
            # Actually move files (implement with caution)
            pass
        
        return {
            "files_analyzed": len(files_to_organize),
            "organization_plan": organization_plan,
            "dry_run": dry_run
        }
    
    # Private helper methods (extracted from original)
    
    def _categorize_file(self, file_path: Path) -> str:
        """Categorize a file based on extension"""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        
        return 'other'
    
    async def _search_by_filename(self, query: str, search_dirs: List[Path]) -> List[Path]:
        """Search by filename matching"""
        results = []
        
        for search_dir in search_dirs:
            if search_dir.exists():
                async for file_path in self._async_scan_directory(search_dir):
                    if file_path.is_file() and file_path.stat().st_size > 0:
                        if query in file_path.name.lower():
                            results.append(file_path)
        
        return results
    
    async def _search_by_content_keywords(self, query: str, search_dirs: List[Path]) -> List[Path]:
        """Search by content keywords (for text files)"""
        results = []
        text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css', '.json']
        
        for search_dir in search_dirs:
            if search_dir.exists():
                async for file_path in self._async_scan_directory(search_dir):
                    if (file_path.is_file() and 
                        file_path.suffix.lower() in text_extensions and
                        file_path.stat().st_size > 0 and
                        file_path.stat().st_size < 1024*1024):  # Max 1MB
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read().lower()
                                if query in content:
                                    results.append(file_path)
                        except:
                            continue
        
        return results
    
    async def _search_by_file_type(self, query: str, search_dirs: List[Path]) -> List[Path]:
        """Search by file type keywords"""
        results = []
        
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
                    async for file_path in self._async_scan_directory(search_dir):
                        if (file_path.is_file() and 
                            file_path.suffix.lower() in extensions and
                            file_path.stat().st_size > 0):
                            results.append(file_path)
        
        return results
    
    async def _search_by_date_context(self, query: str, search_dirs: List[Path]) -> List[Path]:
        """Search by date-related keywords"""
        results = []
        
        if any(word in query for word in ['today', 'recent', 'new', 'latest']):
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    async for file_path in self._async_scan_directory(search_dir):
                        if file_path.is_file() and file_path.stat().st_size > 0:
                            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if mod_time > cutoff_date:
                                results.append(file_path)
        
        elif any(word in query for word in ['old', 'archive', 'backup']):
            cutoff_date = datetime.now() - timedelta(days=90)
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    async for file_path in self._async_scan_directory(search_dir):
                        if file_path.is_file() and file_path.stat().st_size > 0:
                            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if mod_time < cutoff_date:
                                results.append(file_path)
        
        return results
    
    async def _search_by_size_context(self, query: str, search_dirs: List[Path]) -> List[Path]:
        """Search by size-related keywords"""
        results = []
        
        if any(word in query for word in ['large', 'big', 'huge']):
            size_threshold = 10 * 1024 * 1024  # 10MB
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    async for file_path in self._async_scan_directory(search_dir):
                        if (file_path.is_file() and 
                            file_path.stat().st_size > size_threshold):
                            results.append(file_path)
        
        elif any(word in query for word in ['small', 'tiny']):
            size_threshold = 100 * 1024  # 100KB
            
            for search_dir in search_dirs:
                if search_dir.exists():
                    async for file_path in self._async_scan_directory(search_dir):
                        if (file_path.is_file() and 
                            0 < file_path.stat().st_size < size_threshold):
                            results.append(file_path)
        
        return results
    
    def _rank_search_results(self, files: List[Path], query: str, user_id: int) -> List[tuple]:
        """Rank search results by relevance"""
        scored_files = []
        
        for file_path in files:
            score = 0.0
            filename_lower = file_path.name.lower()
            
            # Exact filename match gets highest score
            if query == filename_lower:
                score += 10.0
            elif query in filename_lower:
                score += 5.0
            
            # Query words in filename
            query_words = query.split()
            for word in query_words:
                if word in filename_lower:
                    score += 2.0
            
            # Recent files get bonus
            try:
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                days_old = (datetime.now() - mod_time).days
                if days_old < 7:
                    score += 1.0
                elif days_old < 30:
                    score += 0.5
            except:
                pass
            
            if score > 0:
                scored_files.append((file_path, score))
        
        return sorted(scored_files, key=lambda x: x[1], reverse=True)
    
    def _generate_suggestions(self, file_stats: Dict, size_stats: Dict) -> List[Dict[str, Any]]:
        """Generate smart suggestions"""
        suggestions = []
        
        total_size_mb = sum(size_stats.values()) / (1024*1024)
        
        if total_size_mb > 1000:  # More than 1GB
            largest_category = max(size_stats.items(), key=lambda x: x[1])
            suggestions.append({
                "type": "storage_optimization",
                "message": f"Your {largest_category[0]} files are using {largest_category[1]/(1024*1024):.1f}MB. Consider archiving old files.",
                "priority": "medium"
            })
        
        downloads_files = file_stats.get('other', 0)
        if downloads_files > 20:
            suggestions.append({
                "type": "organization",
                "message": f"You have {downloads_files} uncategorized files. I can help organize them automatically.",
                "priority": "high"
            })
        
        if file_stats.get('archives', 0) > 5:
            suggestions.append({
                "type": "cleanup",
                "message": f"You have {file_stats['archives']} archive files. Some might be safe to remove after extraction.",
                "priority": "low"
            })
        
        return suggestions
    
    def _get_target_directory(self, category: str) -> Optional[Path]:
        """Get target directory for file category"""
        mapping = {
            'images': Path.home() / "Pictures",
            'documents': Path.home() / "Documents",
            'audio': Path.home() / "Music",
            'video': Path.home() / "Videos"
        }
        return mapping.get(category)
    
    async def _async_scan_directory(self, directory: Path):
        """Async generator for scanning directories"""
        try:
            for item in directory.rglob("*"):
                yield item
                # Allow other coroutines to run
                if item.is_file():
                    await asyncio.sleep(0)
        except (OSError, PermissionError):
            return