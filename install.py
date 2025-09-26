#!/usr/bin/env python3
"""
Installation script for Alphabet Learning App
This script checks and installs required dependencies
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        ("Pillow", "PIL"),
        ("pyttsx3", "pyttsx3")
    ]
    
    print("🔍 Checking dependencies...")
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} is already installed")
        except ImportError:
            print(f"📦 Installing {package_name}...")
            if install_package(package_name):
                print(f"✅ {package_name} installed successfully")
            else:
                print(f"❌ Failed to install {package_name}")
                return False
    
    return True

def test_text_to_speech():
    """Test if text-to-speech is working"""
    print("\n🔊 Testing text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("Hello! Text to speech is working.")
        engine.runAndWait()
        print("✅ Text-to-speech is working!")
        return True
    except Exception as e:
        print(f"⚠️  Text-to-speech test failed: {e}")
        print("💡 The app will still work, but without audio.")
        return False

def main():
    """Main installation function"""
    print("🎓 Alphabet Learning App - Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not check_and_install_dependencies():
        print("\n❌ Installation failed!")
        return
    
    # Test text-to-speech
    test_text_to_speech()
    
    print("\n🎉 Installation completed successfully!")
    print("\n🚀 To run the app, use:")
    print("   python main.py")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 