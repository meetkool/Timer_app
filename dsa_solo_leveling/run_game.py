"""
Launch script for DSA Solo Leveling Application

This script handles setup and launches the main application.
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_data_file():
    """Check if the DSA questions data file exists"""
    # Look for the data file in parent directory first
    parent_data_file = "../dsa_queastions.json"
    current_data_file = "dsa_queastions.json"
    
    if os.path.exists(parent_data_file):
        # Copy from parent directory
        import shutil
        shutil.copy2(parent_data_file, current_data_file)
        print("📄 Data file copied from parent directory")
        return True
    elif os.path.exists(current_data_file):
        print("📄 Data file found")
        return True
    else:
        print("❌ DSA questions data file not found!")
        print("📁 Please ensure 'dsa_queastions.json' is in the project directory")
        return False

def main():
    """Main launcher function"""
    print("🎮 DSA Solo Leveling - Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Please run this script from the dsa_solo_leveling directory")
        return
    
    # Install dependencies if needed
    try:
        import pygame
        print("✅ Pygame already installed")
    except ImportError:
        if not install_dependencies():
            return
    
    # Check for data file
    if not check_data_file():
        return
    
    # Launch the application
    print("🚀 Launching DSA Solo Leveling...")
    print("=" * 50)
    
    try:
        from main import main as run_app
        run_app()
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()