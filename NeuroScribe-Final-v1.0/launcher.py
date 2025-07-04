#!/usr/bin/env python3
"""
NeuroScribe PDF Copilot - Launcher Script
This script launches the Streamlit app and can be packaged into an executable.
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def launch_streamlit():
    """Launch the Streamlit application"""
    try:
        # Get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_dir = Path(sys.executable).parent
        else:
            # Running as script
            app_dir = Path(__file__).parent
        
        # Change to the app directory
        os.chdir(app_dir)
        
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8502",
            "--server.headless", "true"
        ]
        
        print("🚀 Launching NeuroScribe PDF Copilot...")
        print(f"📁 Working directory: {app_dir}")
        print("🌐 Opening browser in 3 seconds...")
        
        # Start Streamlit in a separate thread
        def run_streamlit():
            subprocess.run(cmd)
        
        streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
        streamlit_thread.start()
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8502")
        
        print("✅ NeuroScribe PDF Copilot is running!")
        print("🌐 URL: http://localhost:8502")
        print("🔄 Press Ctrl+C to stop the application...")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down NeuroScribe PDF Copilot...")
            
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        input("Press Enter to exit...")

def main():
    print("🚀 Starting NeuroScribe PDF Copilot...")
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Open browser after a short delay
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:8502")
    time.sleep(1)
    
    # Start Streamlit app
    print("📱 Starting Streamlit app...")
    try:
        subprocess.call(["streamlit", "run", "app.py", "--server.port", "8502"])
    except KeyboardInterrupt:
        print("\n👋 NeuroScribe PDF Copilot stopped.")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 