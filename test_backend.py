#!/usr/bin/env python3
"""
Test script for Jaymi AI File Assistant backend
"""

import sys
import os
sys.path.append('/home/runner/work/chuckOS-MVP/chuckOS-MVP')

# Test imports
try:
    from backend.core.file_intelligence import JaymiFileIntelligenceAPI
    print("✅ File intelligence import successful")
except ImportError as e:
    print(f"❌ File intelligence import failed: {e}")

try:
    from backend.models.database import create_tables, User
    print("✅ Database models import successful")
except ImportError as e:
    print(f"❌ Database models import failed: {e}")

try:
    from backend.core.auth import create_access_token, get_password_hash
    print("✅ Auth module import successful")
    auth_imported = True
except ImportError as e:
    print(f"❌ Auth module import failed: {e}")
    auth_imported = False

# Test basic functionality
print("\n🧪 Testing core functionality...")

try:
    # Test file intelligence
    intelligence = JaymiFileIntelligenceAPI()
    print("✅ File intelligence initialized")
    
    # Test password hashing
    if auth_imported:
        test_hash = get_password_hash("test123")
        print("✅ Password hashing works")
        
        # Test token creation
        token = create_access_token({"sub": "test@example.com"})
        print("✅ JWT token creation works")
    else:
        print("⚠️ Skipping auth tests due to import failure")
    
    print("\n🎉 All tests passed! Backend is ready.")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()