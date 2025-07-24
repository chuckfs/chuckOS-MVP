#!/usr/bin/env python3
# /usr/local/bin/jaymi_ai_memory.py

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from jaymi_vault import JaymiVault

class AIMemoryManager:
    """Manages AI memories with vault persistence"""
    
    def __init__(self, vault: JaymiVault):
        self.vault = vault
        self.memory_types = {
            "conversation": {"retention_days": 30, "max_items": 1000},
            "personality_learning": {"retention_days": 365, "max_items": 500},
            "user_preferences": {"retention_days": 365, "max_items": 200},
            "emotional_states": {"retention_days": 7, "max_items": 2000},
            "command_patterns": {"retention_days": 90, "max_items": 300},
            "relationships": {"retention_days": 365, "max_items": 100}
        }
        
        # In-memory cache for performance
        self.memory_cache = {}
        self.cache_max_size = 100
        
    async def store_conversation(self, user_input: str, ai_response: str, 
                               metadata: Dict[str, Any] = None) -> str:
        """Store a conversation exchange"""
        
        conversation_data = {
            "user_input": user_input,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "emotional_analysis": await self._analyze_emotional_content(user_input, ai_response),
            "interaction_id": str(uuid.uuid4())
        }
        
        memory_id = await self._store_memory("conversation", conversation_data)
        
        # Update cache
        self._update_cache("conversation", memory_id, conversation_data)
        
        return memory_id
    
    async def store_personality_learning(self, learning_type: str, learning_data: Dict[str, Any]) -> str:
        """Store personality learning data"""
        
        learning_record = {
            "learning_type": learning_type,
            "data": learning_data,
            "timestamp": datetime.now().isoformat(),
            "confidence": learning_data.get("confidence", 0.5),
            "source": learning_data.get("source", "interaction")
        }
        
        return await self._store_memory("personality_learning", learning_record)
    
    async def store_emotional_state(self, emotional_data: Dict[str, Any]) -> str:
        """Store emotional state snapshot"""
        
        emotional_record = {
            "emotional_state": emotional_data,
            "timestamp": datetime.now().isoformat(),
            "context": emotional_data.get("context", {}),
            "triggers": emotional_data.get("triggers", [])
        }
        
        return await self._store_memory("emotional_states", emotional_record)
    
    async def get_conversation_history(self, limit: int = 10, 
                                     hours_back: int = 24) -> List[Dict[str, Any]]:
        """Retrieve recent conversation history"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        memories = await self._retrieve_memories(
            "conversation", 
            limit=limit,
            since=cutoff_time
        )
        
        return [memory["data"] for memory in memories]
    
    async def get_personality_insights(self, learning_type: str = None) -> List[Dict[str, Any]]:
        """Get personality learning insights"""
        
        memories = await self._retrieve_memories("personality_learning", limit=50)
        
        if learning_type:
            memories = [m for m in memories if m["data"].get("learning_type") == learning_type]
        
        return [memory["data"] for memory in memories]
    
    async def get_emotional_patterns(self, days_back: int = 7) -> Dict[str, Any]:
        """Analyze emotional patterns over time"""
        
        cutoff_time = datetime.now() - timedelta(days=days_back)
        memories = await self._retrieve_memories(
            "emotional_states",
            since=cutoff_time,
            limit=1000
        )
        
        # Analyze patterns
        emotions_over_time = []
        emotion_counts = {}
        
        for memory in memories:
            emotional_data = memory["data"]["emotional_state"]
            timestamp = memory["data"]["timestamp"]
            
            emotions_over_time.append({
                "timestamp": timestamp,
                "emotions": emotional_data
            })
            
            # Count emotion types
            for emotion, intensity in emotional_data.items():
                if emotion not in emotion_counts:
                    emotion_counts[emotion] = []
                emotion_counts[emotion].append(intensity)
        
        # Calculate averages
        emotion_averages = {
            emotion: sum(values) / len(values) 
            for emotion, values in emotion_counts.items()
        }
        
        return {
            "timeline": emotions_over_time,
            "averages": emotion_averages,
            "dominant_emotions": sorted(emotion_averages.items(), 
                                      key=lambda x: x[1], reverse=True)[:3],
            "analysis_period_days": days_back,
            "total_records": len(memories)
        }
    
    async def search_memories(self, query: str, memory_types: List[str] = None, 
                            limit: int = 20) -> List[Dict[str, Any]]:
        """Search memories by content"""
        
        search_types = memory_types or list(self.memory_types.keys())
        results = []
        
        for memory_type in search_types:
            memories = await self._retrieve_memories(memory_type, limit=100)
            
            for memory in memories:
                # Simple text search in memory content
                memory_text = json.dumps(memory["data"]).lower()
                if query.lower() in memory_text:
                    results.append({
                        "memory_type": memory_type,
                        "memory_id": memory["memory_id"],
                        "data": memory["data"],
                        "relevance": self._calculate_relevance(query, memory_text)
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:limit]
    
    async def cleanup_old_memories(self):
        """Clean up old memories based on retention policies"""
        
        for memory_type, policy in self.memory_types.items():
            cutoff_date = datetime.now() - timedelta(days=policy["retention_days"])
            
            # Get old memories
            old_memories = await self._retrieve_memories(
                memory_type,
                before=cutoff_date,
                limit=1000
            )
            
            # Delete old memories
            for memory in old_memories:
                await self.vault.delete_memory(memory["memory_id"])
            
            print(f"🧹 Cleaned up {len(old_memories)} old {memory_type} memories")
    
    async def _store_memory(self, memory_type: str, data: Dict[str, Any]) -> str:
        """Store memory in vault"""
        
        if not self.vault.is_unlocked:
            raise ValueError("Vault must be unlocked to store memories")
        
        memory_record = {
            "memory_type": memory_type,
            "data": data,
            "created": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Store in vault
        memory_id = self.vault.store_memory(memory_type, memory_record)
        
        return memory_id
    
    async def _retrieve_memories(self, memory_type: str, limit: int = 50,
                               since: datetime = None, before: datetime = None) -> List[Dict[str, Any]]:
        """Retrieve memories from vault with filtering"""
        
        # Check cache first
        cache_key = f"{memory_type}_{limit}_{since}_{before}"
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        
        # Search vault
        memories = self.vault.search_memories(memory_type=memory_type)
        
        # Apply filters
        if since:
            memories = [m for m in memories if datetime.fromisoformat(m["timestamp"]) >= since]
        
        if before:
            memories = [m for m in memories if datetime.fromisoformat(m["timestamp"]) <= before]
        
        # Limit results
        memories = memories[:limit]
        
        # Cache results
        self._update_cache(cache_key, None, memories)
        
        return memories
    
    async def _analyze_emotional_content(self, user_input: str, ai_response: str) -> Dict[str, float]:
        """Analyze emotional content of conversation"""
        
        # Simple emotion detection (could be enhanced with ML)
        emotions = {
            "happiness": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "neutral": 0.5
        }
        
        # Analyze user input
        text = (user_input + " " + ai_response).lower()
        
        # Happiness indicators
        happy_words = ["happy", "great", "awesome", "love", "amazing", "wonderful", "excited", "joy"]
        happiness_score = sum(1 for word in happy_words if word in text) / len(happy_words)
        emotions["happiness"] = min(happiness_score, 1.0)
        
        # Sadness indicators
        sad_words = ["sad", "down", "depressed", "unhappy", "upset", "disappointed", "hurt"]
        sadness_score = sum(1 for word in sad_words if word in text) / len(sad_words)
        emotions["sadness"] = min(sadness_score, 1.0)
        
        # Anger indicators
        anger_words = ["angry", "mad", "furious", "annoyed", "frustrated", "irritated"]
        anger_score = sum(1 for word in anger_words if word in text) / len(anger_words)
        emotions["anger"] = min(anger_score, 1.0)
        
        # Normalize to ensure they sum to 1
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    def _update_cache(self, key: str, memory_id: str, data: Any):
        """Update memory cache"""
        
        if len(self.memory_cache) >= self.cache_max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.memory_cache))
            del self.memory_cache[oldest_key]
        
        self.memory_cache[key] = data
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate relevance score for search results"""
        
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        # Simple relevance based on word overlap
        overlap = len(query_words.intersection(content_words))
        return overlap / len(query_words) if query_words else 0.0

# Memory manager instance (to be initialized with vault)
ai_memory = None

def initialize_ai_memory(vault: JaymiVault):
    """Initialize AI memory manager with vault"""
    global ai_memory
    ai_memory = AIMemoryManager(vault)
    return ai_memory
