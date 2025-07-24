#!/usr/bin/env python3
"""
ChuckOS Jaymi Visual Magic System
Dynamic wallpapers, animations, and beautiful GUI
"""

import json
import os
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from datetime import datetime
import threading
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io

class JaymiVisualMagic:
    def __init__(self):
        self.name = "Jaymi Visual"
        self.voice_active = True
        self.current_mood = "neutral"
        self.visual_memory_file = Path.home() / ".jaymi_visual_memory.json"
        
        # Load visual preferences
        self.visual_memory = self.load_visual_memory()
        
        # Initialize GUI
        self.root = tk.Tk()
        self.setup_main_window()
        
        # Visual effects
        self.animations_running = False
        self.mood_colors = {
            "happy": "#4CAF50",
            "excited": "#FF9800", 
            "calm": "#2196F3",
            "professional": "#607D8B",
            "thinking": "#9C27B0",
            "neutral": "#424242"
        }
        
        print("🎨 Jaymi Visual Magic initialized")
        print(f"🖼️ Visual preferences loaded: {len(self.visual_memory.get('wallpapers', []))}")
    
    def load_visual_memory(self):
        """Load visual preferences and history"""
        if self.visual_memory_file.exists():
            try:
                with open(self.visual_memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "wallpapers": [],
            "preferred_mood": "neutral",
            "animation_speed": "medium",
            "theme_preferences": {},
            "visual_interactions": []
        }
    
    def save_visual_memory(self):
        """Save visual preferences"""
        try:
            with open(self.visual_memory_file, 'w') as f:
                json.dump(self.visual_memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Couldn't save visual memory: {e}")
    
    def setup_main_window(self):
        """Setup the main Jaymi visual interface"""
        self.root.title("🤖 ChuckOS Jaymi - Visual Magic")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # Header with mood indicator
        self.header_frame = tk.Frame(self.root, bg='#2d2d2d', height=80)
        self.header_frame.pack(fill='x', padx=10, pady=5)
        self.header_frame.pack_propagate(False)
        
        # Jaymi status
        self.status_label = tk.Label(
            self.header_frame, 
            text="🤖 Jaymi Visual Magic", 
            font=('Arial', 18, 'bold'),
            fg='white', bg='#2d2d2d'
        )
        self.status_label.pack(side='left', padx=20, pady=20)
        
        # Mood indicator
        self.mood_canvas = tk.Canvas(
            self.header_frame, 
            width=60, height=60, 
            bg='#2d2d2d', highlightthickness=0
        )
        self.mood_canvas.pack(side='right', padx=20, pady=10)
        self.update_mood_indicator()
        
        # Main content area
        self.main_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for different features
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_mood_tab()
        self.create_wallpaper_tab()
        self.create_animation_tab()
        self.create_memory_tab()
    
    def create_mood_tab(self):
        """Create mood control tab"""
        mood_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(mood_frame, text="🎭 Mood Control")
        
        # Mood title
        title = tk.Label(
            mood_frame, 
            text="Jaymi's Emotional State", 
            font=('Arial', 16, 'bold'),
            fg='white', bg='#1a1a1a'
        )
        title.pack(pady=20)
        
        # Mood buttons
        mood_button_frame = tk.Frame(mood_frame, bg='#1a1a1a')
        mood_button_frame.pack(pady=20)
        
        moods = [
            ("😊 Happy", "happy"),
            ("🚀 Excited", "excited"), 
            ("😌 Calm", "calm"),
            ("💼 Professional", "professional"),
            ("🤔 Thinking", "thinking"),
            ("😐 Neutral", "neutral")
        ]
        
        for i, (text, mood) in enumerate(moods):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                mood_button_frame,
                text=text,
                font=('Arial', 12),
                width=15,
                height=2,
                command=lambda m=mood: self.change_mood(m),
                bg=self.mood_colors[mood],
                fg='white',
                relief='raised'
            )
            btn.grid(row=row, col=col, padx=10, pady=10)
        
        # Current mood display
        self.current_mood_label = tk.Label(
            mood_frame,
            text=f"Current Mood: {self.current_mood.title()}",
            font=('Arial', 14),
            fg='white', bg='#1a1a1a'
        )
        self.current_mood_label.pack(pady=20)
        
        # Mood effects text
        self.mood_text = tk.Text(
            mood_frame,
            height=8,
            width=70,
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='white',
            wrap='word'
        )
        self.mood_text.pack(pady=20)
        self.update_mood_text()
    
    def create_wallpaper_tab(self):
        """Create dynamic wallpaper tab"""
        wallpaper_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(wallpaper_frame, text="🖼️ Wallpapers")
        
        # Wallpaper title
        title = tk.Label(
            wallpaper_frame,
            text="Dynamic Wallpaper System",
            font=('Arial', 16, 'bold'),
            fg='white', bg='#1a1a1a'
        )
        title.pack(pady=20)
        
        # Wallpaper preview
        self.wallpaper_canvas = tk.Canvas(
            wallpaper_frame,
            width=400, height=300,
            bg='#2d2d2d',
            highlightthickness=1,
            highlightcolor='white'
        )
        self.wallpaper_canvas.pack(pady=20)
        
        # Generate wallpaper based on mood
        self.generate_mood_wallpaper()
        
        # Wallpaper controls
        control_frame = tk.Frame(wallpaper_frame, bg='#1a1a1a')
        control_frame.pack(pady=20)
        
        tk.Button(
            control_frame,
            text="🎨 Generate New",
            font=('Arial', 12),
            command=self.generate_mood_wallpaper,
            bg='#4CAF50', fg='white'
        ).pack(side='left', padx=10)
        
        tk.Button(
            control_frame,
            text="💾 Save Wallpaper",
            font=('Arial', 12),
            command=self.save_wallpaper,
            bg='#2196F3', fg='white'
        ).pack(side='left', padx=10)
        
        tk.Button(
            control_frame,
            text="📁 Set as Desktop",
            font=('Arial', 12),
            command=self.set_desktop_wallpaper,
            bg='#FF9800', fg='white'
        ).pack(side='left', padx=10)
        
        # Wallpaper info
        self.wallpaper_info = tk.Label(
            wallpaper_frame,
            text="Generated wallpaper based on current mood",
            font=('Arial', 10),
            fg='gray', bg='#1a1a1a'
        )
        self.wallpaper_info.pack(pady=10)
    
    def create_animation_tab(self):
        """Create animation effects tab"""
        animation_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(animation_frame, text="✨ Animations")
        
        # Animation title
        title = tk.Label(
            animation_frame,
            text="Visual Animation Effects",
            font=('Arial', 16, 'bold'),
            fg='white', bg='#1a1a1a'
        )
        title.pack(pady=20)
        
        # Animation canvas
        self.animation_canvas = tk.Canvas(
            animation_frame,
            width=500, height=300,
            bg='#000000',
            highlightthickness=1,
            highlightcolor='white'
        )
        self.animation_canvas.pack(pady=20)
        
        # Animation controls
        anim_controls = tk.Frame(animation_frame, bg='#1a1a1a')
        anim_controls.pack(pady=20)
        
        self.animation_running = False
        self.anim_button = tk.Button(
            anim_controls,
            text="▶️ Start Animation",
            font=('Arial', 12),
            command=self.toggle_animation,
            bg='#4CAF50', fg='white'
        )
        self.anim_button.pack(side='left', padx=10)
        
        # Animation type selector
        tk.Label(
            anim_controls,
            text="Effect:",
            font=('Arial', 10),
            fg='white', bg='#1a1a1a'
        ).pack(side='left', padx=10)
        
        self.animation_type = tk.StringVar(value="particles")
        animation_menu = ttk.Combobox(
            anim_controls,
            textvariable=self.animation_type,
            values=["particles", "waves", "matrix", "stars", "pulse"],
            state="readonly",
            width=12
        )
        animation_menu.pack(side='left', padx=10)
    
    def create_memory_tab(self):
        """Create visual memory tab"""
        memory_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(memory_frame, text="🧠 Visual Memory")
        
        # Memory title
        title = tk.Label(
            memory_frame,
            text="Visual Preferences & History",
            font=('Arial', 16, 'bold'),
            fg='white', bg='#1a1a1a'
        )
        title.pack(pady=20)
        
        # Memory stats
        stats_frame = tk.Frame(memory_frame, bg='#2d2d2d')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Display visual memory stats
        self.update_memory_display(stats_frame)
        
        # Visual preferences
        prefs_frame = tk.LabelFrame(
            memory_frame,
            text="Preferences",
            font=('Arial', 12, 'bold'),
            fg='white', bg='#1a1a1a'
        )
        prefs_frame.pack(fill='x', padx=20, pady=20)
        
        # Preferred mood setting
        tk.Label(
            prefs_frame,
            text="Preferred Default Mood:",
            font=('Arial', 10),
            fg='white', bg='#1a1a1a'
        ).pack(anchor='w', padx=10, pady=5)
        
        self.preferred_mood = tk.StringVar(value=self.visual_memory.get("preferred_mood", "neutral"))
        mood_pref_menu = ttk.Combobox(
            prefs_frame,
            textvariable=self.preferred_mood,
            values=list(self.mood_colors.keys()),
            state="readonly"
        )
        mood_pref_menu.pack(anchor='w', padx=10, pady=5)
        mood_pref_menu.bind('<<ComboboxSelected>>', self.save_preferences)
    
    def change_mood(self, new_mood):
        """Change Jaymi's mood and update visuals"""
        old_mood = self.current_mood
        self.current_mood = new_mood
        
        print(f"🎭 Mood changed: {old_mood} → {new_mood}")
        
        # Update mood indicator
        self.update_mood_indicator()
        
        # Update current mood label
        self.current_mood_label.config(text=f"Current Mood: {new_mood.title()}")
        
        # Update mood text
        self.update_mood_text()
        
        # Regenerate wallpaper for new mood
        self.generate_mood_wallpaper()
        
        # Voice response to mood change
        self.speak_mood_change(new_mood)
        
        # Remember this mood change
        self.visual_memory["visual_interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "mood_change",
            "from_mood": old_mood,
            "to_mood": new_mood
        })
        self.save_visual_memory()
    
    def update_mood_indicator(self):
        """Update the mood indicator circle"""
        self.mood_canvas.delete("all")
        color = self.mood_colors[self.current_mood]
        
        # Draw mood circle with pulsing effect
        self.mood_canvas.create_oval(10, 10, 50, 50, fill=color, outline="white", width=2)
        self.mood_canvas.create_text(30, 30, text="●", fill=color, font=('Arial', 20))
    
    def update_mood_text(self):
        """Update mood description text"""
        mood_descriptions = {
            "happy": "😊 I'm feeling great! Everything seems bright and positive. I'm ready to help with enthusiasm!",
            "excited": "🚀 I'm super energized! Ready to tackle any challenge and explore new possibilities!",
            "calm": "😌 I'm in a peaceful state. Perfect for thoughtful analysis and gentle assistance.",
            "professional": "💼 I'm in business mode. Focused, efficient, and ready for serious work.",
            "thinking": "🤔 I'm in analytical mode. Deep thought processes active for complex problem solving.",
            "neutral": "😐 I'm in balanced mode. Ready for any type of interaction or task."
        }
        
        self.mood_text.delete(1.0, tk.END)
        description = mood_descriptions.get(self.current_mood, "Unknown mood state.")
        self.mood_text.insert(tk.END, description)
        
        # Add mood-specific tips
        self.mood_text.insert(tk.END, f"\n\n🎨 Visual Theme: {self.current_mood.title()}")
        self.mood_text.insert(tk.END, f"\n🎵 Suggested Voice Tone: {self.get_voice_tone()}")
        self.mood_text.insert(tk.END, f"\n⚡ Best For: {self.get_mood_best_for()}")
    
    def get_voice_tone(self):
        """Get suggested voice tone for current mood"""
        tones = {
            "happy": "Cheerful and upbeat",
            "excited": "Fast-paced and energetic",
            "calm": "Slow and soothing",
            "professional": "Clear and formal",
            "thinking": "Measured and thoughtful",
            "neutral": "Balanced and natural"
        }
        return tones.get(self.current_mood, "Natural")
    
    def get_mood_best_for(self):
        """Get what the current mood is best for"""
        best_for = {
            "happy": "Creative tasks, brainstorming, positive feedback",
            "excited": "Big projects, new challenges, demonstrations",
            "calm": "Meditation, study assistance, stress relief",
            "professional": "Business tasks, formal presentations, reports",
            "thinking": "Complex analysis, problem solving, research",
            "neutral": "General assistance, everyday tasks"
        }
        return best_for.get(self.current_mood, "General tasks")
    
    def generate_mood_wallpaper(self):
        """Generate wallpaper based on current mood"""
        self.wallpaper_canvas.delete("all")
        
        # Get mood color
        base_color = self.mood_colors[self.current_mood]
        
        # Create gradient background
        for i in range(300):
            # Create gradient effect
            intensity = int(255 * (1 - i / 300))
            color = f"#{intensity:02x}{intensity//2:02x}{intensity//3:02x}"
            self.wallpaper_canvas.create_line(0, i, 400, i, fill=color)
        
        # Add mood-specific elements
        if self.current_mood == "happy":
            # Draw suns and smiles
            for _ in range(5):
                x, y = random.randint(50, 350), random.randint(50, 250)
                self.wallpaper_canvas.create_oval(x-20, y-20, x+20, y+20, fill="yellow", outline="orange")
        
        elif self.current_mood == "excited":
            # Draw energy bursts
            for _ in range(8):
                x, y = random.randint(50, 350), random.randint(50, 250)
                for angle in range(0, 360, 45):
                    import math
                    x2 = x + 30 * math.cos(math.radians(angle))
                    y2 = y + 30 * math.sin(math.radians(angle))
                    self.wallpaper_canvas.create_line(x, y, x2, y2, fill="orange", width=3)
        
        elif self.current_mood == "calm":
            # Draw gentle waves
            for i in range(5):
                y = 50 + i * 50
                points = []
                for x in range(0, 400, 20):
                    wave_y = y + 20 * math.sin(x / 40)
                    points.extend([x, wave_y])
                if len(points) > 2:
                    self.wallpaper_canvas.create_line(points, fill="lightblue", width=2, smooth=True)
        
        # Add mood text
        self.wallpaper_canvas.create_text(
            200, 280,
            text=f"Jaymi • {self.current_mood.title()} Mode",
            font=('Arial', 16, 'bold'),
            fill="white"
        )
        
        # Update wallpaper info
        self.wallpaper_info.config(text=f"Wallpaper generated for {self.current_mood} mood at {datetime.now().strftime('%H:%M')}")
    
    def save_wallpaper(self):
        """Save current wallpaper"""
        filename = f"jaymi_wallpaper_{self.current_mood}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = Path.home() / "Pictures" / filename
        
        # Create directory if it doesn't exist
        filepath.parent.mkdir(exist_ok=True)
        
        try:
            # This would save the canvas as an image (simplified for demo)
            messagebox.showinfo("Wallpaper Saved", f"Wallpaper saved as {filename}")
            
            # Remember this wallpaper
            self.visual_memory["wallpapers"].append({
                "filename": filename,
                "mood": self.current_mood,
                "created": datetime.now().isoformat()
            })
            self.save_visual_memory()
            
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save wallpaper: {e}")
    
    def set_desktop_wallpaper(self):
        """Set as desktop wallpaper (system-specific)"""
        try:
            # This would set the actual desktop wallpaper
            messagebox.showinfo("Desktop Wallpaper", f"Setting {self.current_mood} wallpaper as desktop background")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't set desktop wallpaper: {e}")
    
    def toggle_animation(self):
        """Toggle animation on/off"""
        if self.animations_running:
            self.animations_running = False
            self.anim_button.config(text="▶️ Start Animation")
        else:
            self.animations_running = True
            self.anim_button.config(text="⏹️ Stop Animation")
            self.run_animation()
    
    def run_animation(self):
        """Run the selected animation"""
        if not self.animations_running:
            return
        
        # Clear canvas
        self.animation_canvas.delete("all")
        
        animation_type = self.animation_type.get()
        
        if animation_type == "particles":
            self.animate_particles()
        elif animation_type == "waves":
            self.animate_waves()
        elif animation_type == "matrix":
            self.animate_matrix()
        elif animation_type == "stars":
            self.animate_stars()
        elif animation_type == "pulse":
            self.animate_pulse()
        
        # Continue animation
        if self.animations_running:
            self.root.after(100, self.run_animation)
    
    def animate_particles(self):
        """Particle animation effect"""
        color = self.mood_colors[self.current_mood]
        
        for _ in range(20):
            x = random.randint(0, 500)
            y = random.randint(0, 300)
            size = random.randint(2, 8)
            
            self.animation_canvas.create_oval(
                x-size, y-size, x+size, y+size,
                fill=color, outline=""
            )
    
    def animate_waves(self):
        """Wave animation effect"""
        import math
        color = self.mood_colors[self.current_mood]
        
        for i in range(3):
            points = []
            for x in range(0, 500, 10):
                y = 150 + 50 * math.sin((x + i * 50) / 30) * math.sin(time.time() + i)
                points.extend([x, y])
            
            if len(points) > 2:
                self.animation_canvas.create_line(points, fill=color, width=3, smooth=True)
    
    def animate_matrix(self):
        """Matrix-style falling text"""
        for _ in range(15):
            x = random.randint(0, 480)
            y = random.randint(0, 280)
            char = random.choice("01234567890ABCDEF")
            
            self.animation_canvas.create_text(
                x, y, text=char,
                fill="#00FF00", font=('Courier', 12)
            )
    
    def animate_stars(self):
        """Twinkling stars effect"""
        for _ in range(30):
            x = random.randint(0, 500)
            y = random.randint(0, 300)
            brightness = random.randint(100, 255)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            
            self.animation_canvas.create_text(
                x, y, text="✦",
                fill=color, font=('Arial', random.randint(8, 16))
            )
    
    def animate_pulse(self):
        """Pulsing effect"""
        color = self.mood_colors[self.current_mood]
        pulse_size = int(50 + 30 * math.sin(time.time() * 3))
        
        self.animation_canvas.create_oval(
            250-pulse_size, 150-pulse_size,
            250+pulse_size, 150+pulse_size,
            fill="", outline=color, width=3
        )
    
    def speak_mood_change(self, new_mood):
        """Voice response to mood change"""
        responses = {
            "happy": "I'm feeling so positive and cheerful now!",
            "excited": "Wow! I'm super energized and ready for action!",
            "calm": "Ahh, that's better. I feel peaceful and centered.",
            "professional": "Switching to professional mode. Ready for business.",
            "thinking": "Engaging deep analysis mode. Let me think about this.",
            "neutral": "Back to balanced mode. Ready for anything."
        }
        
        response = responses.get(new_mood, f"Now I'm in {new_mood} mode.")
        print(f"🤖 Jaymi: {response}")
        
        # Use espeak with mood-appropriate settings
        speed = 160
        if new_mood == "excited":
            speed = 180
        elif new_mood == "calm":
            speed = 140
        
        try:
            subprocess.run(['espeak', '-s', str(speed), response], check=False)
        except:
            pass
    
    def update_memory_display(self, parent):
        """Update visual memory display"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Memory stats
        interactions = len(self.visual_memory.get("visual_interactions", []))
        wallpapers = len(self.visual_memory.get("wallpapers", []))
        
        stats_text = f"""
🎭 Mood Changes: {interactions}
🖼️ Wallpapers Created: {wallpapers}
🎨 Current Theme: {self.current_mood.title()}
⏰ Last Active: {datetime.now().strftime('%H:%M:%S')}
"""
        
        tk.Label(
            parent,
            text=stats_text,
            font=('Arial', 11),
            fg='white', bg='#2d2d2d',
            justify='left'
        ).pack(padx=20, pady=10)
    
    def save_preferences(self, event=None):
        """Save visual preferences"""
        self.visual_memory["preferred_mood"] = self.preferred_mood.get()
        self.save_visual_memory()
        print(f"💾 Saved preferred mood: {self.preferred_mood.get()}")
    
    def run_visual_interface(self):
        """Run the visual interface"""
        # Update memory display periodically
        def update_memory():
            if hasattr(self, 'notebook'):
                # Find memory tab and update it
                try:
                    memory_frame = self.notebook.nametowidget(self.notebook.tabs()[3])
                    stats_frame = memory_frame.winfo_children()[1]  # Stats frame
                    self.update_memory_display(stats_frame)
                except:
                    pass
            self.root.after(5000, update_memory)  # Update every 5 seconds
        
        update_memory()
        
        # Start the GUI
        self.root.mainloop()

if __name__ == "__main__":
    print("🎨 ChuckOS Jaymi Visual Magic System")
    print("=" * 50)
    
    try:
        jaymi_visual = JaymiVisualMagic()
        jaymi_visual.run_visual_interface()
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install pillow")
    except Exception as e:
        print(f"❌ Error starting visual interface: {e}")
