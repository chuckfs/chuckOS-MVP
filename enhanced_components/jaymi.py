import asyncio
import multiprocessing as mp
from dataclasses import dataclass
from typing import Dict, Optional, List
import rich.console
import colorama

@dataclass
class JaymiConfig:
    """Core configuration for AI engine"""
    persona_path: str = "/jaymi_secure/personas/active.json"
    memory_path: str = "/jaymi_secure/memory/"
    vault_path: str = "/.chuck_secure/"
    offline_mode: bool = True
    emotional_state: Dict[str, float] = None

class JaymiCore:
    """Main AI integration engine"""
    
    def __init__(self):
        self.config = JaymiConfig()
        self.message_queue = mp.Queue()
        self.memory_manager = MemoryVault()
        self.persona_engine = PersonalityEngine()
        self.nl_parser = NaturalLanguageParser()
        
    async def boot_sequence(self):
        """Initialization with personality check"""
        # Load persona
        persona = self.persona_engine.load_persona()
        
        # Emotional boot decision
        if persona.mood_score > 0.7:
            await self.play_audio("/jaymi_secure/audio/addison_scream.wav")
        else:
            await self.play_audio("/jaymi_secure/audio/ghost_rise.wav")
            
        # Initialize subsystems
        await self.memory_manager.decrypt_vault()
        await self.nl_parser.load_command_mappings()
