#!/bin/bash
# ChuckOS MVP Boot Sequence

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

# Start Jaymi
cd ~/chuckos-mvp/core
python3 jaymi.py
