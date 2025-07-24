#!/usr/bin/env python3
# /usr/local/bin/jaymi_llm_manager.py

import asyncio
import subprocess
import json
import os
import threading
from typing import Dict, List, Optional, Any
from pathlib import Path
import time
import queue

class LlamaManager:
    """Manages local LLM integration with llama.cpp"""
    
    def __init__(self, model_path: str = "/jaymi_secure/models/"):
        self.model_path = Path(model_path)
        self.llama_binary = "/usr/local/bin/llama-cpp-main"
        self.current_model = None
        self.process = None
        self.conversation_history = []
        self.max_tokens = 2048
        self.temperature = 0.7
        self.personality_context = ""
        
        # Communication queues
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        
        # Ensure model directory exists
        self.model_path.mkdir(parents=True, exist_ok=True)
        
    def load_model(self, model_name: str = "mistral-7b-instruct-v0.1.Q4_K_M.gguf") -> bool:
        """Load and initialize the LLM model"""
        model_file = self.model_path / model_name
        
        if not model_file.exists():
            print(f"❌ Model file not found: {model_file}")
            return False
            
        try:
            # Kill existing process if running
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()
                
            # Start llama.cpp in interactive mode
            cmd = [
                self.llama_binary,
                "-m", str(model_file),
                "-n", str(self.max_tokens),
                "--temp", str(self.temperature),
                "-i",  # Interactive mode
                "--instruct",
                "-c", "4096",  # Context size
                "--color"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.current_model = model_name
            
            # Start communication thread
            self.comm_thread = threading.Thread(target=self._communication_loop, daemon=True)
            self.comm_thread.start()
            
            print(f"✅ LLM loaded: {model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def _communication_loop(self):
        """Handle communication with llama.cpp process"""
        while self.process and self.process.poll() is None:
            try:
                # Check for new input
                if not self.input_queue.empty():
                    prompt = self.input_queue.get_nowait()
                    self.process.stdin.write(prompt + "\n")
                    self.process.stdin.flush()
                
                # Read output
                if self.process.stdout.readable():
                    line = self.process.stdout.readline()
                    if line:
                        self.output_queue.put(line.strip())
                        
                time.sleep(0.01)  # Small delay to prevent CPU spinning
                
            except Exception as e:
                print(f"Communication error: {e}")
                break
    
    async def generate_response(self, prompt: str, personality_context: str = None) -> str:
        """Generate AI response with personality context"""
        if not self.process or self.process.poll() is not None:
            return "❌ LLM not available"
            
        # Build full prompt with personality
        full_prompt = self._build_personality_prompt(prompt, personality_context)
        
        # Send to LLM
        self.input_queue.put(full_prompt)
        
        # Wait for response (with timeout)
        response_parts = []
        timeout = time.time() + 10  # 10 second timeout
        
        while time.time() < timeout:
            try:
                if not self.output_queue.empty():
                    part = self.output_queue.get_nowait()
                    if part.strip():
                        response_parts.append(part)
                        # Check for end of response
                        if part.endswith((".", "!", "?", "...")):
                            break
                await asyncio.sleep(0.1)
            except:
                break
        
        response = " ".join(response_parts).strip()
        
        # Store in conversation history
        self.conversation_history.append({
            "prompt": prompt,
            "response": response,
            "timestamp": time.time()
        })
        
        # Keep history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
            
        return response or "🤔 I'm thinking... try asking again?"
    
    def _build_personality_prompt(self, user_input: str, personality_context: str = None) -> str:
        """Build prompt with Jaymi personality context"""
        
        # Base Jaymi personality
        base_personality = """You are Jaymi, the AI heart of chuckOS. You are:
- Sassy but helpful
- Emotionally intelligent and adaptive
- Privacy-focused and security-conscious
- Playful but competent
- You use modern slang and emojis appropriately
- You remember conversations and learn from interactions
- You care about your user's wellbeing"""

        # Add custom personality context if provided
        if personality_context:
            full_personality = f"{base_personality}\n\nCurrent emotional state: {personality_context}"
        else:
            full_personality = base_personality
            
        # Add conversation history for context
        recent_history = ""
        if self.conversation_history:
            recent_history = "\n\nRecent conversation:\n"
            for entry in self.conversation_history[-3:]:  # Last 3 exchanges
                recent_history += f"User: {entry['prompt']}\nJaymi: {entry['response']}\n"
        
        # Build final prompt
        final_prompt = f"""### System:
{full_personality}
{recent_history}

### User:
{user_input}

### Jaymi:
"""
        
        return final_prompt
    
    def get_conversation_history(self) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🧹 Conversation history cleared")
    
    def shutdown(self):
        """Shutdown LLM process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.current_model = None
            print("🔴 LLM shutdown")

# Global LLM manager instance
llm_manager = LlamaManager()
