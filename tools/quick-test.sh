#!/bin/bash
# Quick test of ChuckOS MVP

echo "🧪 Testing ChuckOS MVP Components..."

# Test Python installation
python3 --version || echo "❌ Python3 not found"

# Test dependencies
python3 -c "import speech_recognition; print('✅ speech_recognition working')" 2>/dev/null || echo "❌ speech_recognition missing"
python3 -c "import pyttsx3; print('✅ pyttsx3 working')" 2>/dev/null || echo "❌ pyttsx3 missing"

# Test Jaymi core
echo "🤖 Testing Jaymi AI..."
cd ~/chuckos-mvp/core
python3 -c "from jaymi import JaymiMVP; j = JaymiMVP(); print('✅ Jaymi AI core working')" || echo "❌ Jaymi core has issues"

echo "🎯 Test complete! Ready to build your MVP?"
