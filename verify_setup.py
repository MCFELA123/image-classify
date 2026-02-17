#!/usr/bin/env python3
"""
Setup verification script for Fruit Classification System
Checks all prerequisites and configuration
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python 3.8+ required, found:", f"{version.major}.{version.minor}.{version.micro}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = ['flask', 'openai', 'pymongo', 'PIL', 'dotenv']
    missing = []
    
    for package in required:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print("\n📦 Install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Check for OpenAI API key
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=sk-' in content:
            print("✅ OpenAI API key configured")
            return True
        elif 'OPENAI_API_KEY=your-openai-api-key-here' in content or 'OPENAI_API_KEY=' in content:
            print("⚠️  OpenAI API key not set in .env")
            print("   Add your key: OPENAI_API_KEY=sk-your-key-here")
            print("   Get one at: https://platform.openai.com/api-keys")
            return False
    
    return True

def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        load_dotenv()
        uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running")
        return False

def check_openai_connection():
    """Check if OpenAI API is accessible"""
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or not api_key.startswith('sk-'):
            print("⚠️  Invalid OpenAI API key format")
            return False
        
        client = OpenAI(api_key=api_key)
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("✅ OpenAI API connection successful")
        return True
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        print("   Check your API key and internet connection")
        return False

def check_directories():
    """Check if required directories exist"""
    dirs = ['data/uploads', 'backend', 'frontend']
    all_exist = True
    
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            all_exist = False
    
    return all_exist

def main():
    print("🍎 Fruit Classification System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Project Directories", check_directories),
        ("MongoDB Connection", check_mongodb),
        ("OpenAI API Connection", check_openai_connection),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All checks passed! You're ready to run the application.")
        print("\n🚀 Start the server with:")
        print("   python backend/app.py")
        print("   # or")
        print("   ./run.sh")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n📖 See QUICKSTART.md for detailed setup instructions")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
