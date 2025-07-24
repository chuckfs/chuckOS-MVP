#!/bin/bash
# ChuckOS MVP Boot Sequence (Fixed for venv)

cd ~/chuckos-mvp

# ASCII Art Boot Logo
cat << 'LOGO'
   ________              __   ____  _____
  / ____/ /_  __  ______/ /__/ __ \/ ___/
 / /   / __ \/ / / / ___/ //_/ / / /\__ \ 
/ /___/ / / / /_/ / /__/ ,< / /_/ /___/ / 
\____/_/ /_/\__,_/\___/_/|_|\____//____/  
                                          
    Your Personal AI Operating System
LOGO

echo "🚀 ChuckOS MVP - Booting..."
echo "💫 Initializing Jaymi AI Assistant..."
echo "🔧 Using Python virtual environment..."

# Activate venv and start Jaymi
source venv/bin/activate
cd core
python jaymi.py
