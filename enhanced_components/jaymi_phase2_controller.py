#!/usr/bin/env python3
# /usr/local/bin/jaymi_phase2_controller.py

import asyncio
import sys
import signal
from pathlib import Path

# Import all Phase 2 components
from jaymi_llm_manager import llm_manager
from jaymi_ai_memory import initialize_ai_memory
from jaymi_emotional_engine import emotional_engine
from jaymi_theme_engine import theme_engine
from jaymi_vault import JaymiVault

class Phase2Controller:
    """Main controller for Phase 2 AI integration"""
    
    def __init__(self):
        self.vault = None
        self.ai_memory = None
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
    
    async def initialize(self):
        """Initialize all Phase 2 components"""
        
        print("🚀 Starting chuckOS Phase 2 AI Integration")
        print("=" * 50)
        
        # 1. Initialize vault
        print("🔐 Initializing vault...")
        self.vault = JaymiVault()
        
        if not self.vault.vault_exists():
            print("❌ Vault not found. Please create vault first.")
            return False
        
        # Vault should already be unlocked by boot process
        if not self.vault.is_unlocked:
            print("❌ Vault is locked. Please unlock vault first.")
            return False
        
        # 2. Initialize AI memory
        print("🧠 Initializing AI memory...")
        self.ai_memory = initialize_ai_memory(self.vault)
        
        # 3. Initialize LLM
        print("🤖 Loading language model...")
        if not llm_manager.load_model():
            print("❌ Failed to load LLM. Some features will be limited.")
        
        # 4. Start emotional engine
        print("💫 Starting emotional processing...")
        await emotional_engine.start_emotional_processing()
        
        # 5. Start theme engine
        print("🎨 Starting theme adaptation...")
        await theme_engine.start_personality_adaptation()
        
        # 6. Apply initial theme
        print("🖼️ Applying initial theme...")
        await theme_engine.apply_emotional_theme(force_update=True)
        
        print("✅ Phase 2 initialization complete!")
        print("Jaymi AI core is now active with full personality integration.")
        
        return True
    
    async def run(self):
        """Main execution loop"""
        
        if not await self.initialize():
            return False
        
        self.running = True
        
        print("\n💝 Jaymi is now fully alive!")
        print("- Natural language processing with LLM intelligence")
        print("- Emotional awareness and adaptation")
        print("- Persistent AI memory with vault storage")
        print("- Dynamic theme adaptation to personality")
        print("\nType 'jaymi' to interact or use any natural language commands.")
        
        # Main loop - keep services running
        while self.running:
            try:
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                break
        
        await self.shutdown()
        return True
    
    async def shutdown(self):
        """Shutdown all services gracefully"""
        
        print("\n🛑 Shutting down AI services...")
        
        # Stop theme engine
        await theme_engine.stop_personality_adaptation()
        
        # Stop emotional engine
        await emotional_engine.stop_emotional_processing()
        
        # Shutdown LLM
        llm_manager.shutdown()
        
        # Lock vault
        if self.vault:
            self.vault.lock_vault()
        
        print("👋 Goodbye! Jaymi AI core shutdown complete.")

async def main():
    """Main entry point"""
    controller = Phase2Controller()
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())
