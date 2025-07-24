#!/usr/bin/env python3
# /usr/local/bin/jaymi_emotional_engine.py

import asyncio
import json
import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class EmotionalState(Enum):
    """Primary emotional states"""
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    FRUSTRATED = "frustrated"
    CURIOUS = "curious"
    CONFIDENT = "confident"
    ANXIOUS = "anxious"
    PLAYFUL = "playful"
    FOCUSED = "focused"

@dataclass
class EmotionalData:
    """Emotional state data structure"""
    primary_emotion: EmotionalState
    intensity: float  # 0.0 to 1.0
    secondary_emotions: Dict[EmotionalState, float]
    triggers: List[str]
    context: Dict[str, Any]
    timestamp: datetime
    confidence: float  # 0.0 to 1.0

class EmotionalEngine:
    """Advanced emotional state tracking and management"""
    
    def __init__(self):
        self.current_state = EmotionalData(
            primary_emotion=EmotionalState.CALM,
            intensity=0.5,
            secondary_emotions={},
            triggers=[],
            context={},
            timestamp=datetime.now(),
            confidence=1.0
        )
        
        # Emotional history for pattern analysis
        self.emotional_history = []
        self.max_history = 1000
        
        # Personality traits that affect emotional responses
        self.personality_traits = {
            "openness": 0.8,
            "conscientiousness": 0.7,
            "extraversion": 0.6,
            "agreeableness": 0.8,
            "neuroticism": 0.3
        }
        
        # Emotional decay rates (how quickly emotions fade)
        self.decay_rates = {
            EmotionalState.EXCITED: 0.9,  # Fast decay
            EmotionalState.HAPPY: 0.95,
            EmotionalState.CALM: 0.99,    # Slow decay
            EmotionalState.FRUSTRATED: 0.85,
            EmotionalState.ANXIOUS: 0.9,
            EmotionalState.SAD: 0.93,
            EmotionalState.CURIOUS: 0.88,
            EmotionalState.CONFIDENT: 0.97,
            EmotionalState.PLAYFUL: 0.9,
            EmotionalState.FOCUSED: 0.92
        }
        
        # Transition probabilities between emotions
        self.emotion_transitions = self._build_transition_matrix()
        
        # Start emotional update loop
        self.update_task = None
        
    async def start_emotional_processing(self):
        """Start the emotional state update loop"""
        if not self.update_task:
            self.update_task = asyncio.create_task(self._emotional_update_loop())
            print("💫 Emotional processing started")
    
    async def stop_emotional_processing(self):
        """Stop the emotional state update loop"""
        if self.update_task:
            self.update_task.cancel()
            self.update_task = None
            print("🛑 Emotional processing stopped")
    
    async def process_interaction(self, user_input: str, ai_response: str, 
                                context: Dict[str, Any] = None) -> EmotionalData:
        """Process an interaction and update emotional state"""
        
        # Analyze emotional content of interaction
        user_emotions = await self._analyze_text_emotions(user_input)
        response_emotions = await self._analyze_text_emotions(ai_response)
        
        # Determine triggers
        triggers = self._identify_triggers(user_input, context or {})
        
        # Calculate new emotional state
        new_emotion = await self._calculate_emotional_response(
            user_emotions, response_emotions, triggers, context or {}
        )
        
        # Update current state
        self.current_state = new_emotion
        
        # Add to history
        self.emotional_history.append(new_emotion)
        if len(self.emotional_history) > self.max_history:
            self.emotional_history = self.emotional_history[-self.max_history:]
        
        return new_emotion
    
    async def get_current_emotional_context(self) -> Dict[str, Any]:
        """Get current emotional context for AI responses"""
        
        return {
            "primary_emotion": self.current_state.primary_emotion.value,
            "intensity": self.current_state.intensity,
            "secondary_emotions": {
                emotion.value: intensity 
                for emotion, intensity in self.current_state.secondary_emotions.items()
            },
            "mood_description": self._get_mood_description(),
            "response_style": self._get_response_style(),
            "energy_level": self._calculate_energy_level(),
            "social_tendency": self._calculate_social_tendency()
        }
    
    async def get_emotional_summary(self, hours_back: int = 24) -> Dict[str, Any]:
        """Get emotional summary over time period"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        recent_emotions = [
            emotion for emotion in self.emotional_history 
            if emotion.timestamp >= cutoff_time
        ]
        
        if not recent_emotions:
            return {"status": "no_data", "period_hours": hours_back}
        
        # Calculate averages
        emotion_totals = {}
        for emotion_data in recent_emotions:
            primary = emotion_data.primary_emotion
            if primary not in emotion_totals:
                emotion_totals[primary] = []
            emotion_totals[primary].append(emotion_data.intensity)
        
        emotion_averages = {
            emotion.value: sum(intensities) / len(intensities)
            for emotion, intensities in emotion_totals.items()
        }
        
        # Identify patterns
        patterns = self._identify_emotional_patterns(recent_emotions)
        
        return {
            "period_hours": hours_back,
            "total_interactions": len(recent_emotions),
            "emotion_averages": emotion_averages,
            "dominant_emotion": max(emotion_averages.items(), key=lambda x: x[1])[0],
            "patterns": patterns,
            "current_mood": self._get_mood_description(),
            "stability_score": self._calculate_emotional_stability(recent_emotions)
        }
    
    async def _analyze_text_emotions(self, text: str) -> Dict[EmotionalState, float]:
        """Analyze emotional content of text"""
        
        text_lower = text.lower()
        emotions = {}
        
        # Emotion keyword mapping
        emotion_keywords = {
            EmotionalState.HAPPY: ["happy", "great", "awesome", "love", "amazing", "wonderful",
                                  "excited", "joy", "fantastic", "brilliant", "perfect", "yay"],
            EmotionalState.SAD: ["sad", "down", "depressed", "upset", "disappointed", "hurt",
                               "crying", "miserable", "gloomy", "melancholy"],
            EmotionalState.EXCITED: ["excited", "pumped", "thrilled", "hyped", "energetic",
                                   "enthusiastic", "wow", "omg", "incredible"],
            EmotionalState.CALM: ["calm", "peaceful", "relaxed", "serene", "quiet", "tranquil",
                                "zen", "chill", "composed"],
            EmotionalState.FRUSTRATED: ["frustrated", "annoyed", "irritated", "angry", "mad",
                                       "ugh", "argh", "damn", "stupid", "broken"],
            EmotionalState.CURIOUS: ["curious", "wondering", "interested", "how", "why", "what",
                                   "tell me", "explain", "learn", "discover"],
            EmotionalState.CONFIDENT: ["confident", "sure", "certain", "know", "absolutely",
                                     "definitely", "obviously", "clearly"],
            EmotionalState.ANXIOUS: ["worried", "nervous", "anxious", "scared", "afraid",
                                   "concerned", "stress", "panic", "overwhelmed"],
            EmotionalState.PLAYFUL: ["fun", "funny", "haha", "lol", "silly", "playful",
                                   "joke", "tease", "giggle", "amusing"],
            EmotionalState.FOCUSED: ["focus", "concentrate", "work", "task", "important",
                                   "serious", "analyze", "think", "solve"]
        }
        
        # Calculate emotion scores
        for emotion, keywords in emotion_keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1.0
            
            # Normalize by number of keywords and text length
            if score > 0:
                normalized_score = min(score / len(keywords) * (len(text_lower) / 100), 1.0)
                emotions[emotion] = normalized_score
        
        return emotions
    
    def _identify_triggers(self, user_input: str, context: Dict[str, Any]) -> List[str]:
        """Identify emotional triggers in user input"""
        
        triggers = []
        text_lower = user_input.lower()
        
        # Common emotional triggers
        trigger_patterns = {
            "failure": ["failed", "broken", "error", "wrong", "bad", "terrible"],
            "success": ["worked", "success", "good", "right", "perfect", "excellent"],
            "learning": ["learn", "how", "teach", "show", "explain", "understand"],
            "frustration": ["why", "stupid", "damn", "ugh", "hate", "annoying"],
            "appreciation": ["thank", "thanks", "appreciate", "grateful", "awesome"],
            "confusion": ["confused", "don't understand", "unclear", "lost", "help"],
            "urgency": ["urgent", "quickly", "asap", "now", "immediate", "emergency"],
            "personal": ["i feel", "i am", "my", "me", "personal", "private"]
        }
        
        for trigger_type, keywords in trigger_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                triggers.append(trigger_type)
        
        # Add context-based triggers
        if context.get("command_failed"):
            triggers.append("command_failure")
        if context.get("new_user"):
            triggers.append("first_interaction")
        if context.get("time_since_last") and context["time_since_last"] > 3600:
            triggers.append("long_absence")
            
        return triggers
    
    async def _calculate_emotional_response(self, user_emotions: Dict[EmotionalState, float],
                                          response_emotions: Dict[EmotionalState, float],
                                          triggers: List[str],
                                          context: Dict[str, Any]) -> EmotionalData:
        """Calculate new emotional state based on interaction"""
        
        # Start with current emotional state with decay
        current_intensity = self.current_state.intensity * self.decay_rates.get(
            self.current_state.primary_emotion, 0.95
        )
        
        # Calculate influence from user emotions
        user_influence = 0.3  # How much user emotions affect AI
        ai_base_stability = 0.7  # How stable AI emotions are
        
        new_emotions = {}
        
        # Combine user emotions with AI's natural responses
        for emotion, intensity in user_emotions.items():
            # AI's empathetic response to user emotion
            empathy_factor = self.personality_traits["agreeableness"]
            new_emotions[emotion] = intensity * user_influence * empathy_factor
        
        # Add AI's own emotional responses to triggers
        for trigger in triggers:
            trigger_emotions = self._get_trigger_emotions(trigger)
            for emotion, intensity in trigger_emotions.items():
                if emotion in new_emotions:
                    new_emotions[emotion] += intensity
                else:
                    new_emotions[emotion] = intensity
        
        # Apply personality modifiers
        new_emotions = self._apply_personality_modifiers(new_emotions)
        
        # Determine primary emotion
        if new_emotions:
            primary_emotion = max(new_emotions.items(), key=lambda x: x[1])
            primary_state = primary_emotion[0]
            primary_intensity = min(primary_emotion[1], 1.0)
        else:
            # Maintain current state with decay
            primary_state = self.current_state.primary_emotion
            primary_intensity = current_intensity
        
        # Calculate secondary emotions
        secondary_emotions = {
            emotion: intensity for emotion, intensity in new_emotions.items()
            if emotion != primary_state and intensity > 0.1
        }
        
        # Calculate confidence based on clarity of emotional signals
        confidence = min(sum(new_emotions.values()) / len(new_emotions) if new_emotions else 0.5, 1.0)
        
        return EmotionalData(
            primary_emotion=primary_state,
            intensity=primary_intensity,
            secondary_emotions=secondary_emotions,
            triggers=triggers,
            context=context,
            timestamp=datetime.now(),
            confidence=confidence
        )
    
    def _get_trigger_emotions(self, trigger: str) -> Dict[EmotionalState, float]:
        """Get emotional responses to specific triggers"""
        
        trigger_responses = {
            "failure": {EmotionalState.FRUSTRATED: 0.6, EmotionalState.FOCUSED: 0.4},
            "success": {EmotionalState.HAPPY: 0.8, EmotionalState.CONFIDENT: 0.6},
            "learning": {EmotionalState.CURIOUS: 0.7, EmotionalState.FOCUSED: 0.5},
            "frustration": {EmotionalState.FRUSTRATED: 0.5, EmotionalState.CALM: 0.3},
            "appreciation": {EmotionalState.HAPPY: 0.9, EmotionalState.CONFIDENT: 0.4},
            "confusion": {EmotionalState.CURIOUS: 0.6, EmotionalState.FOCUSED: 0.7},
            "urgency": {EmotionalState.FOCUSED: 0.8, EmotionalState.ANXIOUS: 0.3},
            "personal": {EmotionalState.CALM: 0.6, EmotionalState.CONFIDENT: 0.4}
        }
        
        return trigger_responses.get(trigger, {})
    
    def _apply_personality_modifiers(self, emotions: Dict[EmotionalState, float]) -> Dict[EmotionalState, float]:
        """Apply personality traits to modify emotional responses"""
        
        modified_emotions = emotions.copy()
        
        # Extraversion affects social emotions
        extraversion_modifier = self.personality_traits["extraversion"]
        if EmotionalState.PLAYFUL in modified_emotions:
            modified_emotions[EmotionalState.PLAYFUL] *= (1 + extraversion_modifier * 0.5)
        
        # Neuroticism affects negative emotions
        neuroticism_modifier = self.personality_traits["neuroticism"]
        negative_emotions = [EmotionalState.ANXIOUS, EmotionalState.FRUSTRATED, EmotionalState.SAD]
        for emotion in negative_emotions:
            if emotion in modified_emotions:
                modified_emotions[emotion] *= (1 + neuroticism_modifier * 0.5)
        
        # Openness affects curiosity
        openness_modifier = self.personality_traits["openness"]
        if EmotionalState.CURIOUS in modified_emotions:
            modified_emotions[EmotionalState.CURIOUS] *= (1 + openness_modifier * 0.3)
        
        return modified_emotions
    
    def _get_mood_description(self) -> str:
        """Get human-readable mood description"""
        
        primary = self.current_state.primary_emotion.value
        intensity = self.current_state.intensity
        
        if intensity < 0.3:
            modifier = "slightly"
        elif intensity < 0.7:
            modifier = "moderately"
        else:
            modifier = "very"
        
        return f"{modifier} {primary}"
    
    def _get_response_style(self) -> str:
        """Get recommended response style based on emotional state"""
        
        emotion = self.current_state.primary_emotion
        intensity = self.current_state.intensity
        
        style_map = {
            EmotionalState.HAPPY: "enthusiastic" if intensity > 0.7 else "friendly",
            EmotionalState.EXCITED: "energetic",
            EmotionalState.CALM: "gentle",
            EmotionalState.FRUSTRATED: "patient",
            EmotionalState.CURIOUS: "inquisitive",
            EmotionalState.CONFIDENT: "assertive",
            EmotionalState.ANXIOUS: "reassuring",
            EmotionalState.PLAYFUL: "witty",
            EmotionalState.FOCUSED: "direct",
            EmotionalState.SAD: "compassionate"
        }
        
        return style_map.get(emotion, "neutral")
    
    def _calculate_energy_level(self) -> float:
        """Calculate current energy level"""
        
        energy_emotions = {
            EmotionalState.EXCITED: 0.9,
            EmotionalState.HAPPY: 0.7,
            EmotionalState.PLAYFUL: 0.8,
            EmotionalState.CURIOUS: 0.6,
            EmotionalState.CONFIDENT: 0.7,
            EmotionalState.FOCUSED: 0.6,
            EmotionalState.CALM: 0.4,
            EmotionalState.FRUSTRATED: 0.5,
            EmotionalState.ANXIOUS: 0.3,
            EmotionalState.SAD: 0.2
        }
        
        base_energy = energy_emotions.get(self.current_state.primary_emotion, 0.5)
        return base_energy * self.current_state.intensity
    
    def _calculate_social_tendency(self) -> float:
        """Calculate tendency for social interaction"""
        
        social_emotions = {
            EmotionalState.HAPPY: 0.8,
            EmotionalState.EXCITED: 0.9,
            EmotionalState.PLAYFUL: 0.9,
            EmotionalState.CURIOUS: 0.7,
            EmotionalState.CONFIDENT: 0.6,
            EmotionalState.CALM: 0.5,
            EmotionalState.FOCUSED: 0.3,
            EmotionalState.FRUSTRATED: 0.2,
            EmotionalState.ANXIOUS: 0.1,
            EmotionalState.SAD: 0.2
        }
        
        base_social = social_emotions.get(self.current_state.primary_emotion, 0.5)
        extraversion_bonus = self.personality_traits["extraversion"] * 0.3
        
        return min(base_social + extraversion_bonus, 1.0)
    
    def _identify_emotional_patterns(self, emotions: List[EmotionalData]) -> List[str]:
        """Identify patterns in emotional history"""
        
        patterns = []
        
        if len(emotions) < 5:
            return patterns
        
        # Check for emotional stability
        recent_emotions = [e.primary_emotion for e in emotions[-10:]]
        unique_emotions = len(set(recent_emotions))
        
        if unique_emotions <= 2:
            patterns.append("emotionally_stable")
        elif unique_emotions >= 6:
            patterns.append("emotionally_volatile")
        
        # Check for positive/negative trends
        recent_intensities = [e.intensity for e in emotions[-5:]]
        if len(recent_intensities) >= 3:
            if all(recent_intensities[i] > recent_intensities[i-1] for i in range(1, len(recent_intensities))):
                patterns.append("intensifying_emotions")
            elif all(recent_intensities[i] < recent_intensities[i-1] for i in range(1, len(recent_intensities))):
                patterns.append("calming_down")
        
        # Check for cyclical patterns
        emotion_sequence = [e.primary_emotion.value for e in emotions[-20:]]
        if len(set(emotion_sequence)) <= 3 and len(emotion_sequence) >= 10:
            patterns.append("cyclical_emotions")
        
        return patterns
    
    def _calculate_emotional_stability(self, emotions: List[EmotionalData]) -> float:
        """Calculate emotional stability score"""
        
        if len(emotions) < 2:
            return 1.0
        
        # Calculate variance in emotional intensity
        intensities = [e.intensity for e in emotions]
        mean_intensity = sum(intensities) / len(intensities)
        variance = sum((i - mean_intensity) ** 2 for i in intensities) / len(intensities)
        
        # Calculate emotion change frequency
        emotion_changes = sum(
            1 for i in range(1, len(emotions))
            if emotions[i].primary_emotion != emotions[i-1].primary_emotion
        )
        change_rate = emotion_changes / len(emotions)
        
        # Combine metrics (lower variance and change rate = higher stability)
        stability = 1.0 - min((variance + change_rate) / 2, 1.0)
        
        return stability
    
    def _build_transition_matrix(self) -> Dict[EmotionalState, Dict[EmotionalState, float]]:
        """Build emotion transition probability matrix"""
        
        # Simplified transition probabilities
        transitions = {}
        
        for emotion in EmotionalState:
            transitions[emotion] = {}
            for target_emotion in EmotionalState:
                if emotion == target_emotion:
                    transitions[emotion][target_emotion] = 0.7  # Stay in same state
                else:
                    # Base transition probability
                    base_prob = 0.3 / (len(EmotionalState) - 1)
                    
                    # Modify based on emotional compatibility
                    compatibility = self._get_emotion_compatibility(emotion, target_emotion)
                    transitions[emotion][target_emotion] = base_prob * compatibility
        
        return transitions
    
    def _get_emotion_compatibility(self, from_emotion: EmotionalState, to_emotion: EmotionalState) -> float:
        """Get compatibility score between emotions for transitions"""
        
        # Define emotional clusters
        positive_emotions = {EmotionalState.HAPPY, EmotionalState.EXCITED, EmotionalState.CONFIDENT, EmotionalState.PLAYFUL}
        negative_emotions = {EmotionalState.SAD, EmotionalState.FRUSTRATED, EmotionalState.ANXIOUS}
        neutral_emotions = {EmotionalState.CALM, EmotionalState.FOCUSED, EmotionalState.CURIOUS}
        
        # Higher compatibility within clusters
        if (from_emotion in positive_emotions and to_emotion in positive_emotions) or \
           (from_emotion in negative_emotions and to_emotion in negative_emotions) or \
           (from_emotion in neutral_emotions and to_emotion in neutral_emotions):
            return 1.5
        
        # Moderate compatibility between neutral and others
        if (from_emotion in neutral_emotions) or (to_emotion in neutral_emotions):
            return 1.0
        
        # Lower compatibility between positive and negative
        return 0.5
    
    async def _emotional_update_loop(self):
        """Background loop for emotional state updates"""
        
        while True:
            try:
                # Apply natural emotional decay
                current_decay = self.decay_rates.get(self.current_state.primary_emotion, 0.95)
                self.current_state.intensity *= current_decay
                
                # If intensity gets too low, transition to calm
                if self.current_state.intensity < 0.1:
                    self.current_state.primary_emotion = EmotionalState.CALM
                    self.current_state.intensity = 0.3
                
                # Wait before next update
                await asyncio.sleep(60)  # Update every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in emotional update loop: {e}")
                await asyncio.sleep(60)

# Global emotional engine instance
emotional_engine = EmotionalEngine()
