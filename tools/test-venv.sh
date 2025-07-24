#!/bin/bash
# Test ChuckOS MVP with virtual environment

cd ~/chuckos-mvp
source venv/bin/activate

echo "🧪 Testing ChuckOS MVP Components (Virtual Environment)..."

# Test Python installation
python --version

# Test dependencies
python -c "import speech_recognition; print('✅ speech_recognition working')" 2>/dev/null || echo "❌ speech_recognition missing"
python -c "import pyttsx3; print('✅ pyttsx3 working')" 2>/dev/null || echo "❌ pyttsx3 missing"
python -c "import pyaudio; print('✅ pyaudio working')" 2>/dev/null || echo "❌ pyaudio missing"

# Test Jaymi core
echo "🤖 Testing Jaymi AI..."
cd core
python -c "from jaymi import JaymiMVP; j = JaymiMVP(); print('✅ Jaymi AI core working')" 2>/dev/null || echo "❌ Jaymi core has issues"

echo "🎯 Test complete! Ready to test Jaymi?"
