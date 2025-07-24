#!/bin/bash
# Install ChuckOS MVP Dependencies

echo "📦 Installing ChuckOS MVP Dependencies..."

# Update system
sudo apt update || sudo pacman -Sy || sudo yum update

# Install Python dependencies
pip3 install --user speech_recognition pyttsx3 pyaudio

# Install system dependencies
if command -v apt &> /dev/null; then
    sudo apt install -y python3-pyaudio espeak espeak-data
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm python-pyaudio espeak espeak-ng
elif command -v yum &> /dev/null; then
    sudo yum install -y python3-pyaudio espeak espeak-ng
fi

echo "✅ Dependencies installed!"
echo "🚀 Run: cd ~/chuckos-mvp && bash boot/startup.sh"
