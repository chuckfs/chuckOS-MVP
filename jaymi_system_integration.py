#!/usr/bin/env python3
"""
ChuckOS Jaymi System Integration Control
Complete system control, monitoring, and automation
"""

import json
import os
import subprocess
import time
import psutil
import platform
from pathlib import Path
from datetime import datetime, timedelta
import threading
import schedule
from collections import defaultdict

class JaymiSystemIntegration:
    def __init__(self):
        self.name = "Jaymi System Control"
        self.voice_active = True
        self.system_memory_file = Path.home() / ".jaymi_system_memory.json"
        
        # Load system control memory
        self.system_memory = self.load_system_memory()
        
        # System monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Automation rules
        self.automation_rules = []
        
        print("⚙️ Jaymi System Integration initialized")
        print(f"🖥️ System: {platform.system()} {platform.release()}")
        print(f"🧠 System patterns learned: {len(self.system_memory.get('performance_history', []))}")
    
    def load_system_memory(self):
        """Load system control memory"""
        if self.system_memory_file.exists():
            try:
                with open(self.system_memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "performance_history": [],
            "automation_rules": [],
            "system_preferences": {},
            "maintenance_schedule": {},
            "alerts_sent": [],
            "optimization_applied": []
        }
    
    def save_system_memory(self):
        """Save system control memory"""
        try:
            with open(self.system_memory_file, 'w') as f:
                json.dump(self.system_memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Couldn't save system memory: {e}")
    
    def speak(self, text, speed=160):
        """Make Jaymi speak with system authority"""
        print(f"🤖 Jaymi: {text}")
        if self.voice_active:
            try:
                subprocess.run(['espeak', '-s', str(speed), '-p', '65', text], check=False)
            except:
                pass
        time.sleep(0.2)
    
    def comprehensive_system_analysis(self):
        """Complete system health and performance analysis"""
        print("\n🔍 COMPREHENSIVE SYSTEM ANALYSIS")
        print("=" * 50)
        
        self.speak("Performing comprehensive system analysis and health check.")
        
        # CPU Analysis
        print("🔍 CPU Analysis...")
        cpu_percent = psutil.cpu_percent(interval=2)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        print(f"   💻 CPU Usage: {cpu_percent}%")
        print(f"   🔢 CPU Cores: {cpu_count}")
        if cpu_freq:
            print(f"   ⚡ CPU Frequency: {cpu_freq.current:.0f}MHz")
        
        # Memory Analysis
        print("\n🔍 Memory Analysis...")
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        print(f"   🧠 RAM Usage: {memory.percent}% ({memory.used/1024**3:.1f}GB / {memory.total/1024**3:.1f}GB)")
        print(f"   💿 Swap Usage: {swap.percent}% ({swap.used/1024**3:.1f}GB / {swap.total/1024**3:.1f}GB)")
        
        # Disk Analysis
        print("\n🔍 Disk Analysis...")
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        print(f"   📀 Disk Usage: {disk_usage.percent}% ({disk_usage.used/1024**3:.1f}GB / {disk_usage.total/1024**3:.1f}GB)")
        if disk_io:
            print(f"   📈 Disk I/O: {disk_io.read_count} reads, {disk_io.write_count} writes")
        
        # Network Analysis
        print("\n🔍 Network Analysis...")
        try:
            network_io = psutil.net_io_counters()
            print(f"   🌐 Network I/O: {network_io.bytes_sent/1024**2:.1f}MB sent, {network_io.bytes_recv/1024**2:.1f}MB received")
        except:
            print("   🌐 Network statistics unavailable")
        
        # Process Analysis
        print("\n🔍 Process Analysis...")
        processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
        
        # Sort by CPU usage
        processes.sort(key=lambda p: p.info['cpu_percent'] or 0, reverse=True)
        
        print("   🔥 Top CPU processes:")
        for proc in processes[:5]:
            if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 0:
                print(f"      {proc.info['name']}: {proc.info['cpu_percent']:.1f}% CPU, {proc.info['memory_percent']:.1f}% RAM")
        
        # System health assessment
        health_score = self.calculate_system_health_score(cpu_percent, memory.percent, disk_usage.percent)
        
        print(f"\n📊 SYSTEM HEALTH SCORE: {health_score}/100")
        
        if health_score >= 80:
            health_status = "Excellent"
            health_color = "🟢"
        elif health_score >= 60:
            health_status = "Good"
            health_color = "🟡"
        else:
            health_status = "Needs Attention"
            health_color = "🔴"
        
        print(f"{health_color} Status: {health_status}")
        
        # Store performance data
        performance_data = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk_usage.percent,
            "health_score": health_score
        }
        
        self.system_memory["performance_history"].append(performance_data)
        
        # Keep only last 100 records
        if len(self.system_memory["performance_history"]) > 100:
            self.system_memory["performance_history"] = self.system_memory["performance_history"][-100:]
        
        self.save_system_memory()
        
        # Generate recommendations
        recommendations = self.generate_system_recommendations(cpu_percent, memory.percent, disk_usage.percent)
        
        if recommendations:
            print(f"\n💡 SYSTEM RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        self.speak(f"System analysis complete! Health score: {health_score} out of 100. Status: {health_status}.")
        
        return {
            'health_score': health_score,
            'status': health_status,
            'recommendations': recommendations
        }
    
    def calculate_system_health_score(self, cpu_percent, memory_percent, disk_percent):
        """Calculate overall system health score"""
        score = 100
        
        # CPU penalty
        if cpu_percent > 80:
            score -= 30
        elif cpu_percent > 60:
            score -= 15
        elif cpu_percent > 40:
            score -= 5
        
        # Memory penalty
        if memory_percent > 90:
            score -= 25
        elif memory_percent > 80:
            score -= 15
        elif memory_percent > 70:
            score -= 10
        
        # Disk penalty
        if disk_percent > 95:
            score -= 20
        elif disk_percent > 85:
            score -= 10
        elif disk_percent > 75:
            score -= 5
        
        return max(0, score)
    
    def generate_system_recommendations(self, cpu_percent, memory_percent, disk_percent):
        """Generate intelligent system recommendations"""
        recommendations = []
        
        if cpu_percent > 80:
            recommendations.append("🔥 High CPU usage detected. Consider closing unnecessary applications.")
        
        if memory_percent > 80:
            recommendations.append("🧠 High memory usage. Consider restarting memory-intensive applications.")
        
        if disk_percent > 90:
            recommendations.append("📀 Disk space critically low. Clean up old files or move data to external storage.")
        elif disk_percent > 80:
            recommendations.append("📀 Disk space getting low. Consider cleaning up temporary files.")
        
        # Check for long-running processes
        try:
            boot_time = psutil.boot_time()
            uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            
            if uptime.days > 7:
                recommendations.append("🔄 System has been running for over a week. Consider restarting for optimal performance.")
        except:
            pass
        
        return recommendations
    
    def system_optimization(self):
        """Perform system optimization tasks"""
        print("\n⚡ SYSTEM OPTIMIZATION")
        print("=" * 30)
        
        self.speak("Performing system optimization to improve performance.")
        
        optimization_tasks = []
        
        # Clear system caches
        print("🧹 Clearing system caches...")
        try:
            # Clear package caches (Ubuntu/Debian)
            if platform.system() == "Linux":
                result = subprocess.run(['which', 'apt'], capture_output=True)
                if result.returncode == 0:
                    subprocess.run(['sudo', 'apt', 'autoclean'], check=False)
                    subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=False)
                    optimization_tasks.append("Cleared APT caches")
            
            # Clear user caches
            cache_dirs = [
                Path.home() / ".cache",
                Path("/tmp")
            ]
            
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    # Count files before cleanup
                    file_count = sum(1 for _ in cache_dir.rglob("*") if _.is_file())
                    
                    if file_count > 100:  # Only clean if there are many files
                        try:
                            subprocess.run(['find', str(cache_dir), '-type', 'f', '-atime', '+7', '-delete'], 
                                         check=False, capture_output=True)
                            optimization_tasks.append(f"Cleaned {cache_dir.name} directory")
                        except:
                            pass
        
        except Exception as e:
            print(f"   ⚠️ Cache cleanup error: {e}")
        
        # Memory optimization
        print("🧠 Optimizing memory usage...")
        try:
            # Sync and drop caches (Linux)
            if platform.system() == "Linux":
                subprocess.run(['sync'], check=False)
                optimization_tasks.append("Synchronized file system")
        except:
            pass
        
        # Check for system updates
        print("🔄 Checking for system updates...")
        try:
            if platform.system() == "Linux":
                result = subprocess.run(['apt', 'list', '--upgradable'], 
                                      capture_output=True, text=True, check=False)
                if result.stdout and "upgradable" in result.stdout:
                    upgradable_count = result.stdout.count('\n') - 1
                    if upgradable_count > 0:
                        optimization_tasks.append(f"Found {upgradable_count} available updates")
        except:
            pass
        
        # Performance tuning suggestions
        print("⚡ Analyzing performance settings...")
        
        # Check swap usage
        swap = psutil.swap_memory()
        if swap.percent > 50:
            optimization_tasks.append("High swap usage detected - consider adding more RAM")
        
        # Check startup programs (approximation)
        try:
            autostart_dir = Path.home() / ".config/autostart"
            if autostart_dir.exists():
                autostart_count = len(list(autostart_dir.glob("*.desktop")))
                if autostart_count > 10:
                    optimization_tasks.append(f"Many startup programs ({autostart_count}) - consider disabling unused ones")
        except:
            pass
        
        print(f"\n✅ OPTIMIZATION COMPLETE")
        
        if optimization_tasks:
            print("🛠️ Tasks performed:")
            for task in optimization_tasks:
                print(f"   • {task}")
        
        # Store optimization record
        self.system_memory["optimization_applied"].append({
            "timestamp": datetime.now().isoformat(),
            "tasks": optimization_tasks
        })
        self.save_system_memory()
        
        self.speak(f"System optimization complete! Performed {len(optimization_tasks)} optimization tasks.")
        
        return optimization_tasks
    
    def smart_system_control(self, command):
        """Process natural language system control commands"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['restart', 'reboot']):
            return self.system_restart_request()
        
        elif any(word in command_lower for word in ['shutdown', 'power off', 'turn off']):
            return self.system_shutdown_request()
        
        elif any(word in command_lower for word in ['sleep', 'suspend', 'hibernate']):
            return self.system_sleep_request()
        
        elif any(word in command_lower for word in ['update', 'upgrade']):
            return self.system_update_request()
        
        elif any(word in command_lower for word in ['clean', 'cleanup', 'optimize']):
            return self.system_optimization()
        
        elif any(word in command_lower for word in ['monitor', 'watch', 'track']):
            return self.start_system_monitoring()
        
        elif any(word in command_lower for word in ['process', 'kill', 'stop']):
            return self.process_management_help()
        
        else:
            self.speak(f"I understand you want to {command}, but I need more specific instructions for system control.")
            return "need_clarification"
    
    def system_restart_request(self):
        """Handle system restart request"""
        self.speak("System restart requested. I recommend saving all work first.")
        print("🔄 System restart requested")
        print("⚠️ This would restart your computer. Use 'sudo reboot' to execute.")
        return "restart_requested"
    
    def system_shutdown_request(self):
        """Handle system shutdown request"""
        self.speak("System shutdown requested. Make sure to save all important work.")
        print("⏹️ System shutdown requested")
        print("⚠️ This would shut down your computer. Use 'sudo shutdown now' to execute.")
        return "shutdown_requested"
    
    def system_sleep_request(self):
        """Handle system sleep request"""
        self.speak("Putting system to sleep mode.")
        print("😴 System sleep requested")
        try:
            if platform.system() == "Linux":
                subprocess.run(['systemctl', 'suspend'], check=False)
                return "sleep_executed"
        except:
            print("⚠️ Sleep command failed. Try 'sudo systemctl suspend'")
            return "sleep_failed"
    
    def system_update_request(self):
        """Handle system update request"""
        self.speak("Checking for system updates.")
        print("🔄 Checking for system updates...")
        
        try:
            if platform.system() == "Linux":
                # Check for updates
                result = subprocess.run(['apt', 'list', '--upgradable'], 
                                      capture_output=True, text=True, check=False)
                
                if result.stdout and "upgradable" in result.stdout:
                    lines = result.stdout.strip().split('\n')
                    upgradable_count = len([line for line in lines if "/" in line]) - 1
                    
                    if upgradable_count > 0:
                        print(f"📦 {upgradable_count} packages can be upgraded")
                        print("💡 Run 'sudo apt update && sudo apt upgrade' to install updates")
                        self.speak(f"Found {upgradable_count} available updates.")
                        return "updates_available"
                    else:
                        print("✅ System is up to date")
                        self.speak("Your system is already up to date.")
                        return "up_to_date"
        except Exception as e:
            print(f"❌ Update check failed: {e}")
            return "update_check_failed"
    
    def start_system_monitoring(self):
        """Start continuous system monitoring"""
        if self.monitoring_active:
            print("📊 System monitoring is already active")
            return "already_monitoring"
        
        print("📊 Starting system monitoring...")
        self.speak("Starting continuous system monitoring.")
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self.monitor_system_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        return "monitoring_started"
    
    def monitor_system_loop(self):
        """Continuous system monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect current metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                disk_percent = psutil.disk_usage('/').percent
                
                # Check for alerts
                alerts = []
                
                if cpu_percent > 90:
                    alerts.append(f"🔥 High CPU usage: {cpu_percent:.1f}%")
                
                if memory_percent > 90:
                    alerts.append(f"🧠 High memory usage: {memory_percent:.1f}%")
                
                if disk_percent > 95:
                    alerts.append(f"📀 Disk space critically low: {disk_percent:.1f}%")
                
                # Display alerts
                if alerts:
                    print(f"\n⚠️ SYSTEM ALERTS [{datetime.now().strftime('%H:%M:%S')}]:")
                    for alert in alerts:
                        print(f"   {alert}")
                    
                    # Store alerts
                    for alert in alerts:
                        self.system_memory["alerts_sent"].append({
                            "timestamp": datetime.now().isoformat(),
                            "alert": alert
                        })
                
                # Brief status update every 30 seconds
                if int(time.time()) % 30 == 0:
                    print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] CPU: {cpu_percent:.1f}% | RAM: {memory_percent:.1f}% | Disk: {disk_percent:.1f}%")
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)
    
    def stop_system_monitoring(self):
        """Stop system monitoring"""
        if not self.monitoring_active:
            print("📊 System monitoring is not active")
            return "not_monitoring"
        
        self.monitoring_active = False
        print("📊 System monitoring stopped")
        self.speak("System monitoring stopped.")
        return "monitoring_stopped"
    
    def process_management_help(self):
        """Help with process management"""
        print("🔍 PROCESS MANAGEMENT HELP")
        print("=" * 30)
        
        # Show current top processes
        processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
        processes.sort(key=lambda p: p.info['cpu_percent'] or 0, reverse=True)
        
        print("🔥 Top processes by CPU usage:")
        for i, proc in enumerate(processes[:10], 1):
            if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 0:
                print(f"   {i}. PID {proc.info['pid']}: {proc.info['name']} - {proc.info['cpu_percent']:.1f}% CPU")
        
        print("\n💡 Process management commands:")
        print("   • 'ps aux' - List all processes")
        print("   • 'top' or 'htop' - Interactive process viewer")
        print("   • 'kill <PID>' - Terminate process by ID")
        print("   • 'killall <name>' - Terminate all processes by name")
        
        self.speak("Here's information about current processes and management commands.")
        return "process_help_shown"
    
    def show_system_history(self):
        """Show system performance history"""
        print("\n📈 SYSTEM PERFORMANCE HISTORY")
        print("=" * 40)
        
        history = self.system_memory.get("performance_history", [])
        
        if not history:
            print("No performance history available yet.")
            self.speak("No system performance history available. Run system analysis first.")
            return
        
        # Show recent history
        recent_history = history[-10:]  # Last 10 records
        
        print("🕒 Recent Performance (last 10 records):")
        for record in recent_history:
            timestamp = datetime.fromisoformat(record["timestamp"])
            print(f"   {timestamp.strftime('%b %d %H:%M')} - Health: {record['health_score']}/100 (CPU: {record['cpu_percent']:.1f}%, RAM: {record['memory_percent']:.1f}%, Disk: {record['disk_percent']:.1f}%)")
        
        # Calculate averages
        if len(history) > 1:
            avg_health = sum(r["health_score"] for r in history) / len(history)
            avg_cpu = sum(r["cpu_percent"] for r in history) / len(history)
            avg_memory = sum(r["memory_percent"] for r in history) / len(history)
            
            print(f"\n📊 Performance Averages:")
            print(f"   Average Health Score: {avg_health:.1f}/100")
            print(f"   Average CPU Usage: {avg_cpu:.1f}%")
            print(f"   Average Memory Usage: {avg_memory:.1f}%")
        
        # Show optimization history
        optimizations = self.system_memory.get("optimization_applied", [])
        if optimizations:
            print(f"\n🛠️ Recent Optimizations:")
            for opt in optimizations[-3:]:  # Last 3 optimizations
                timestamp = datetime.fromisoformat(opt["timestamp"])
                print(f"   {timestamp.strftime('%b %d %H:%M')}: {len(opt['tasks'])} tasks")
        
        avg_health = sum(h.get('health_score', 0) for h in history) / len(history) if history else 0
        self.speak(f"System history shows {len(history)} performance records with an average health score of {avg_health:.0f} out of 100.")
    
    def interactive_system_control(self):
        """Interactive system control interface"""
        print("\n⚙️ JAYMI SYSTEM INTEGRATION CONTROL")
        print("=" * 60)
        print("Commands:")
        print("  'analyze' - Comprehensive system analysis")
        print("  'optimize' - Perform system optimization")
        print("  'monitor start/stop' - System monitoring control")
        print("  'history' - Show performance history")
        print("  'control [command]' - Natural language system control")
        print("  'restart/shutdown/sleep' - Power management")
        print("  'update' - Check for system updates")
        print("  'quit' - Exit")
        
        while True:
            try:
                command = input("\n💬 System Command: ").strip().lower()
                
                if command == 'quit':
                    if self.monitoring_active:
                        self.stop_system_monitoring()
                    self.speak("System control session complete!")
                    break
                    
                elif command == 'analyze':
                    self.comprehensive_system_analysis()
                    
                elif command == 'optimize':
                    self.system_optimization()
                    
                elif command == 'monitor start':
                    self.start_system_monitoring()
                    
                elif command == 'monitor stop':
                    self.stop_system_monitoring()
                    
                elif command == 'history':
                    self.show_system_history()
                    
                elif command.startswith('control '):
                    system_command = command[8:]  # Remove 'control '
                    self.smart_system_control(system_command)
                    
                elif command in ['restart', 'reboot']:
                    self.system_restart_request()
                    
                elif command in ['shutdown', 'power off']:
                    self.system_shutdown_request()
                    
                elif command == 'sleep':
                    self.system_sleep_request()
                    
                elif command == 'update':
                    self.system_update_request()
                    
                else:
                    print("Unknown command. Type 'analyze', 'optimize', 'monitor start/stop', 'history', or 'quit'")
                    
            except KeyboardInterrupt:
                if self.monitoring_active:
                    self.stop_system_monitoring()
                self.speak("System control interrupted!")
                break

if __name__ == "__main__":
    print("⚙️ ChuckOS Jaymi System Integration Control")
    print("=" * 50)
    
    try:
        jaymi = JaymiSystemIntegration()
        jaymi.interactive_system_control()
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install psutil schedule")
    except Exception as e:
        print(f"❌ Error starting system control: {e}")
