#!/usr/bin/env python3
"""
Jaymi AI File Assistant - API Demo
Demonstrates the core functionality of the SaaS application
"""

import requests
import json
import time
import sys

# API Configuration
API_BASE = "http://localhost:8000"

def demo_api():
    print("🤖 Jaymi AI File Assistant - API Demo")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ API is running and healthy")
        else:
            print("❌ API health check failed")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to API. Make sure the backend is running on port 8000")
        print("💡 Run: python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
        return
    
    print()
    
    # Test user registration
    print("👤 Testing User Registration...")
    user_data = {
        "email": "demo@jaymiAI.com",
        "password": "demo123456",
        "full_name": "Demo User"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/register", json=user_data)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data["access_token"]
            user = auth_data["user"]
            print(f"✅ User registered successfully: {user['email']}")
            print(f"📊 Subscription: {user['subscription_tier'].upper()}")
            print(f"🔑 Token: {token[:20]}...")
        else:
            # Might already exist, try login
            print("⚠️ Registration failed, trying login...")
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response = requests.post(f"{API_BASE}/auth/login", json=login_data)
            if response.status_code == 200:
                auth_data = response.json()
                token = auth_data["access_token"]
                user = auth_data["user"]
                print(f"✅ User logged in successfully: {user['email']}")
            else:
                print("❌ Authentication failed")
                return
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    print()
    
    # Set up headers with token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test smart search
    print("🔍 Testing Smart File Search...")
    search_queries = [
        "find my photos",
        "recent documents", 
        "large files",
        "music files"
    ]
    
    for query in search_queries:
        print(f"  🔎 Searching: '{query}'")
        search_data = {"query": query}
        
        try:
            response = requests.post(f"{API_BASE}/files/search", json=search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                print(f"    ✅ Found {results['total_found']} files in {results['search_time']}s")
                
                # Show first few results
                for i, file in enumerate(results['results'][:3]):
                    print(f"       {i+1}. {file['filename']} ({file['category']}) - {file['size_mb']:.1f}MB")
            else:
                print(f"    ❌ Search failed: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Search error: {e}")
        
        time.sleep(0.5)  # Rate limiting
    
    print()
    
    # Test file analysis
    print("📊 Testing File System Analysis...")
    try:
        response = requests.get(f"{API_BASE}/files/analyze", headers=headers)
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Analysis complete!")
            print(f"   📁 Total files: {analysis['total_files']:,}")
            print(f"   💾 Total size: {analysis['total_size_mb']:.1f} MB")
            print(f"   📂 Categories found: {len(analysis['categories'])}")
            
            # Show top categories
            if analysis['categories']:
                print("   🏆 Top categories:")
                sorted_categories = sorted(analysis['categories'].items(), key=lambda x: x[1], reverse=True)
                for category, count in sorted_categories[:3]:
                    size_mb = analysis['category_sizes'].get(category, 0)
                    print(f"      {category}: {count} files ({size_mb:.1f} MB)")
            
            # Show suggestions
            if analysis['suggestions']:
                print("   💡 AI Suggestions:")
                for suggestion in analysis['suggestions'][:2]:
                    print(f"      {suggestion['type']}: {suggestion['message']}")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analysis error: {e}")
    
    print()
    
    # Test insights
    print("💡 Testing AI Insights...")
    try:
        response = requests.get(f"{API_BASE}/files/insights", headers=headers)
        if response.status_code == 200:
            insights_data = response.json()
            insights = insights_data.get('insights', [])
            print(f"✅ Retrieved {len(insights)} insights:")
            
            for insight in insights:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(insight['priority'], '⚪')
                print(f"   {priority_emoji} {insight['title']}: {insight['message']}")
        else:
            print(f"❌ Insights failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Insights error: {e}")
    
    print()
    
    # Test user profile
    print("👤 Testing User Profile...")
    try:
        response = requests.get(f"{API_BASE}/user/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profile retrieved:")
            print(f"   📧 Email: {profile['email']}")
            print(f"   💎 Subscription: {profile['subscription_tier'].upper()}")
            print(f"   🔍 Searches this month: {profile['searches_this_month']}")
            print(f"   📁 Files analyzed: {profile['files_analyzed']}")
        else:
            print(f"❌ Profile failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Profile error: {e}")
    
    print()
    print("🎉 API Demo Complete!")
    print()
    print("🌐 Try the web interface:")
    print("   Frontend: http://localhost:3000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    demo_api()