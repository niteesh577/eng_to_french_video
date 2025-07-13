#!/usr/bin/env python3
"""
Setup script for AI Video Dubber project.
Installs dependencies and sets up the project structure.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def check_system_dependencies():
    """Check if system dependencies are installed."""
    print("Checking system dependencies...")
    
    # Check ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ ffmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ffmpeg not found. Please install ffmpeg:")
        print("   Mac: brew install ffmpeg")
        print("   Ubuntu: sudo apt install ffmpeg")
        return False
    
    # Check tesseract
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
        print("✅ tesseract found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ tesseract not found. Please install tesseract:")
        print("   Mac: brew install tesseract")
        print("   Ubuntu: sudo apt install tesseract-ocr")
        return False
    
    return True

def create_env_template():
    """Create .env template if it doesn't exist."""
    env_path = ".env"
    if not os.path.exists(env_path):
        print("Creating .env template...")
        with open(env_path, "w") as f:
            f.write("# Add your API keys here\n")
            f.write("GOOGLE_API_KEY=your_gemini_api_key_here\n")
            f.write("ELEVENLABS_API_KEY=your_elevenlabs_api_key_here\n")
        print("✅ .env template created. Please add your API keys.")

def main():
    print("🚀 Setting up AI Video Dubber...")
    
    # Install Python dependencies
    if not install_requirements():
        return
    
    # Check system dependencies
    if not check_system_dependencies():
        print("⚠️  Some system dependencies are missing. Please install them and run setup again.")
        return
    
    # Create .env template
    create_env_template()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add your API keys to .env file")
    print("2. Run: streamlit run streamlit_app.py")
    print("3. Upload a video and enjoy!")

if __name__ == "__main__":
    main() 