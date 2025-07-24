#!/usr/bin/env python3
# /usr/local/bin/jaymi_theme_engine.py

import asyncio
import json
import subprocess
import zipfile
import os
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from jaymi_emotional_engine import emotional_engine, EmotionalState

class PersonalityThemeEngine:
    """Theme engine that adapts to AI personality and emotional state"""
    
    def __init__(self):
        self.theme_base_path = Path("/jaymi_secure/themes")
        self.active_themes_path = Path("/tmp/jaymi_active_themes")
        self.xfce_config_path = Path.home() / ".config" / "xfce4"
        self.audio_path = Path("/jaymi_secure/audio")
        
        # Current theme state
        self.active_theme = None
        self.current_personality_mode = "ghost_phoenix"
        self.last_emotion_check = 0
        self.emotion_check_interval = 30  # seconds
        
        # Theme adaptation settings
        self.auto_adapt_enabled = True
        self.adaptation_sensitivity = 0.7  # 0.0 to 1.0
        
        # Initialize directories
        self._initialize_directories()
        
        # Load theme configurations
        self.theme_configs = self._load_theme_configs()
        
        # Start adaptation loop
        self.adaptation_task = None
    
    def _initialize_directories(self):
        """Initialize theme directories"""
        directories = [
            self.theme_base_path,
            self.active_themes_path,
            self.audio_path,
            self.theme_base_path / "installed",
            self.theme_base_path / "community",
            self.theme_base_path / "custom"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        print("📁 Theme directories initialized")
    
    def _load_theme_configs(self) -> Dict[str, Any]:
        """Load theme configuration files"""
        
        configs = {}
        
        # Load built-in theme configs
        builtin_themes = {
            "ghost_phoenix": self._create_ghost_phoenix_config(),
            "dark_mode": self._create_dark_mode_config(),
            "light_mode": self._create_light_mode_config(),
            "hacker_mode": self._create_hacker_mode_config(),
            "kawaii_mode": self._create_kawaii_mode_config()
        }
        
        configs.update(builtin_themes)
        
        # Load custom theme configs
        for theme_dir in self.theme_base_path.glob("*/"):
            if theme_dir.is_dir():
                config_file = theme_dir / "theme_config.json"
                if config_file.exists():
                    try:
                        with open(config_file) as f:
                            theme_config = json.load(f)
                            configs[theme_dir.name] = theme_config
                    except Exception as e:
                        print(f"❌ Failed to load theme config {theme_dir.name}: {e}")
        
        return configs
    
    async def start_personality_adaptation(self):
        """Start automatic theme adaptation based on personality"""
        if not self.adaptation_task:
            self.adaptation_task = asyncio.create_task(self._adaptation_loop())
            print("🎨 Theme personality adaptation started")
    
    async def stop_personality_adaptation(self):
        """Stop automatic theme adaptation"""
        if self.adaptation_task:
            self.adaptation_task.cancel()
            self.adaptation_task = None
            print("🛑 Theme personality adaptation stopped")
    
    async def apply_emotional_theme(self, force_update: bool = False):
        """Apply theme based on current emotional state"""
        
        current_time = time.time()
        if not force_update and (current_time - self.last_emotion_check) < self.emotion_check_interval:
            return
        
        # Get current emotional context
        emotional_context = await emotional_engine.get_current_emotional_context()
        
        # Determine appropriate theme
        target_theme = self._select_theme_for_emotion(emotional_context)
        
        if target_theme != self.active_theme or force_update:
            await self._apply_theme(target_theme, emotional_context)
            self.active_theme = target_theme
        
        self.last_emotion_check = current_time
    
    def _select_theme_for_emotion(self, emotional_context: Dict[str, Any]) -> str:
        """Select appropriate theme based on emotional state"""
        
        primary_emotion = emotional_context.get("primary_emotion", "calm")
        intensity = emotional_context.get("intensity", 0.5)
        energy_level = emotional_context.get("energy_level", 0.5)
        
        # Theme selection logic
        if primary_emotion == "excited" and intensity > 0.7:
            return "kawaii_mode"
        elif primary_emotion == "frustrated" and intensity > 0.6:
            return "dark_mode"
        elif primary_emotion == "focused" or (primary_emotion == "curious" and intensity > 0.6):
            return "hacker_mode"
        elif energy_level < 0.3:
            return "light_mode"
        else:
            return "ghost_phoenix"  # Default theme
    
    async def _apply_theme(self, theme_name: str, emotional_context: Dict[str, Any]):
        """Apply a complete theme with emotional adaptations"""
        
        if theme_name not in self.theme_configs:
            print(f"❌ Theme not found: {theme_name}")
            return
        
        theme_config = self.theme_configs[theme_name]
        
        print(f"🎨 Applying theme: {theme_name}")
        
        # Apply visual elements
        await self._apply_visual_theme(theme_config, emotional_context)
        
        # Apply audio elements
        await self._apply_audio_theme(theme_config, emotional_context)
        
        # Apply behavioral adaptations
        await self._apply_behavioral_theme(theme_config, emotional_context)
        
        print(f"✅ Theme applied: {theme_name}")
    
    async def _apply_visual_theme(self, theme_config: Dict[str, Any], 
                                emotional_context: Dict[str, Any]):
        """Apply visual theme elements"""
        
        visual_config = theme_config.get("visual", {})
        
        # XFCE theme settings
        xfce_commands = []
        
        if "gtk_theme" in visual_config:
            xfce_commands.append(
                f"xfconf-query -c xsettings -p /Net/ThemeName -s {visual_config['gtk_theme']}"
            )
        
        if "window_theme" in visual_config:
            xfce_commands.append(
                f"xfconf-query -c xfwm4 -p /general/theme -s {visual_config['window_theme']}"
            )
        
        if "icon_theme" in visual_config:
            xfce_commands.append(
                f"xfconf-query -c xsettings -p /Net/IconThemeName -s {visual_config['icon_theme']}"
            )
        
        # Wallpaper with emotional adaptation
        wallpaper = self._select_emotional_wallpaper(visual_config, emotional_context)
        if wallpaper:
            xfce_commands.append(
                f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s {wallpaper}"
            )
        
        # Execute XFCE commands
        for command in xfce_commands:
            try:
                subprocess.run(command.split(), check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to apply visual setting: {command} - {e}")
        
        # Terminal colors
        if "terminal_colors" in visual_config:
            await self._apply_terminal_colors(visual_config["terminal_colors"])
    
    async def _apply_audio_theme(self, theme_config: Dict[str, Any], 
                               emotional_context: Dict[str, Any]):
        """Apply audio theme elements"""
        
        audio_config = theme_config.get("audio", {})
        
        # Select emotional audio
        audio_file = self._select_emotional_audio(audio_config, emotional_context)
        
        if audio_file:
            # Play theme audio if appropriate
            intensity = emotional_context.get("intensity", 0.5)
            if intensity > 0.6:  # Only play audio for strong emotions
                await self._play_audio(audio_file)
    
    async def _apply_behavioral_theme(self, theme_config: Dict[str, Any], 
                                    emotional_context: Dict[str, Any]):
        """Apply behavioral theme adaptations"""
        
        behavior_config = theme_config.get("behavior", {})
        
        # Update personality engine settings based on theme
        if "response_style" in behavior_config:
            # This would update the personality engine's response style
            pass
        
        if "interaction_patterns" in behavior_config:
            # This would update how Jaymi interacts based on theme
            pass
    
    def _select_emotional_wallpaper(self, visual_config: Dict[str, Any], 
                                  emotional_context: Dict[str, Any]) -> Optional[str]:
        """Select wallpaper based on emotional state"""
        
        wallpapers = visual_config.get("wallpapers", {})
        primary_emotion = emotional_context.get("primary_emotion", "calm")
        
        # Try to find emotion-specific wallpaper
        if primary_emotion in wallpapers:
            return wallpapers[primary_emotion]
        
        # Fallback to default
        return wallpapers.get("default")
    
    def _select_emotional_audio(self, audio_config: Dict[str, Any], 
                              emotional_context: Dict[str, Any]) -> Optional[str]:
        """Select audio based on emotional state"""
        
        sounds = audio_config.get("sounds", {})
        primary_emotion = emotional_context.get("primary_emotion", "calm")
        intensity = emotional_context.get("intensity", 0.5)
        
        # Select based on emotion and intensity
        emotion_sounds = sounds.get(primary_emotion, {})
        
        if intensity > 0.7 and "high_intensity" in emotion_sounds:
            return emotion_sounds["high_intensity"]
        elif intensity < 0.3 and "low_intensity" in emotion_sounds:
            return emotion_sounds["low_intensity"]
        else:
            return emotion_sounds.get("default")
    
    async def _play_audio(self, audio_file: str):
        """Play audio file"""
        
        audio_path = self.audio_path / audio_file
        
        if audio_path.exists():
            try:
                # Use sox to play audio (non-blocking)
                subprocess.Popen(
                    ["sox", str(audio_path), "-d"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception as e:
                print(f"❌ Failed to play audio: {e}")
    
    async def _apply_terminal_colors(self, color_config: Dict[str, str]):
        """Apply terminal color scheme"""
        
        # Update .Xresources for terminal colors
        xresources_path = Path.home() / ".Xresources"
        
        color_settings = []
        for color_name, color_value in color_config.items():
            color_settings.append(f"*{color_name}: {color_value}")
        
        # Append to .Xresources
        try:
            with open(xresources_path, "a") as f:
                f.write("\n! Jaymi theme colors\n")
                f.write("\n".join(color_settings))
                f.write("\n")
            
            # Reload .Xresources
            subprocess.run(["xrdb", "-merge", str(xresources_path)], 
                         capture_output=True)
        except Exception as e:
            print(f"❌ Failed to apply terminal colors: {e}")
    
    async def install_theme_pack(self, theme_zip_path: Path) -> bool:
        """Install a theme pack from ZIP file"""
        
        try:
            with zipfile.ZipFile(theme_zip_path) as z:
                # Extract to temporary directory
                temp_dir = self.active_themes_path / f"temp_{int(time.time())}"
                z.extractall(temp_dir)
                
                # Validate theme structure
                if not (temp_dir / "theme_config.json").exists():
                    print("❌ Invalid theme pack: missing theme_config.json")
                    shutil.rmtree(temp_dir)
                    return False
                
                # Load theme config
                with open(temp_dir / "theme_config.json") as f:
                    theme_config = json.load(f)
                
                theme_name = theme_config.get("name", "unknown_theme")
                
                # Install to themes directory
                install_path = self.theme_base_path / "installed" / theme_name
                if install_path.exists():
                    shutil.rmtree(install_path)
                
                shutil.move(str(temp_dir), str(install_path))
                
                # Update theme configs
                self.theme_configs[theme_name] = theme_config
                
                print(f"✅ Theme installed: {theme_name}")
                return True
                
        except Exception as e:
            print(f"❌ Failed to install theme pack: {e}")
            return False
    
    async def _adaptation_loop(self):
        """Background loop for theme adaptation"""
        
        while True:
            try:
                if self.auto_adapt_enabled:
                    await self.apply_emotional_theme()
                
                await asyncio.sleep(self.emotion_check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in theme adaptation loop: {e}")
                await asyncio.sleep(self.emotion_check_interval)
    
    # Theme configuration creators
    def _create_ghost_phoenix_config(self) -> Dict[str, Any]:
        """Create Ghost Phoenix theme configuration"""
        return {
            "name": "Ghost Phoenix",
            "description": "Default Jaymi personality theme",
            "visual": {
                "gtk_theme": "Adwaita-dark",
                "window_theme": "Default",
                "icon_theme": "Papirus-Dark",
                "wallpapers": {
                    "default": "/jaymi_secure/themes/ghost_phoenix/wallpaper.jpg",
                    "excited": "/jaymi_secure/themes/ghost_phoenix/wallpaper_excited.jpg",
                    "calm": "/jaymi_secure/themes/ghost_phoenix/wallpaper_calm.jpg"
                },
                "terminal_colors": {
                    "background": "#1a1a1a",
                    "foreground": "#ffffff",
                    "color0": "#2e3436",
                    "color8": "#555753"
                }
            },
            "audio": {
                "sounds": {
                    "excited": {
                        "high_intensity": "addison_scream.wav",
                        "default": "ghost_rise.wav"
                    },
                    "calm": {
                        "default": "ripple_silent.wav"
                    },
                    "default": "ghost_rise.wav"
                }
            },
            "behavior": {
                "response_style": "adaptive",
                "interaction_patterns": ["witty", "helpful", "emotionally_aware"]
            }
        }
    
    def _create_dark_mode_config(self) -> Dict[str, Any]:
        """Create dark mode theme configuration"""
        return {
            "name": "Dark Mode",
            "description": "Dark theme for focused work or frustration",
            "visual": {
                "gtk_theme": "Adwaita-dark",
                "window_theme": "Default-dark",
                "icon_theme": "Papirus-Dark",
                "wallpapers": {
                    "default": "/usr/share/backgrounds/dark_abstract.jpg"
                },
                "terminal_colors": {
                    "background": "#000000",
                    "foreground": "#00ff00"
                }
            },
            "audio": {
                "sounds": {
                    "frustrated": {
                        "default": "calm_breathing.wav"
                    }
                }
            }
        }
    
    def _create_light_mode_config(self) -> Dict[str, Any]:
        """Create light mode theme configuration"""
        return {
            "name": "Light Mode",
            "description": "Light theme for calm, peaceful interactions",
            "visual": {
                "gtk_theme": "Adwaita",
                "window_theme": "Default",
                "icon_theme": "Papirus",
                "wallpapers": {
                    "default": "/usr/share/backgrounds/light_abstract.jpg"
                }
            }
        }
    
    def _create_hacker_mode_config(self) -> Dict[str, Any]:
        """Create hacker mode theme configuration"""
        return {
            "name": "Hacker Mode",
            "description": "Matrix-style theme for focused coding",
            "visual": {
                "gtk_theme": "Adwaita-dark",
                "terminal_colors": {
                    "background": "#000000",
                    "foreground": "#00ff00"
                }
            }
        }
    
    def _create_kawaii_mode_config(self) -> Dict[str, Any]:
        """Create kawaii mode theme configuration"""
        return {
            "name": "Kawaii Mode",
            "description": "Cute theme for excited, playful moods",
            "visual": {
                "gtk_theme": "Adwaita",
                "icon_theme": "Papirus",
                "wallpapers": {
                    "default": "/jaymi_secure/themes/kawaii/cute_wallpaper.jpg"
                }
            },
            "audio": {
                "sounds": {
                    "excited": {
                        "default": "kawaii_notification.wav"
                    }
                }
            }
        }

# Global theme engine instance
theme_engine = PersonalityThemeEngine()
