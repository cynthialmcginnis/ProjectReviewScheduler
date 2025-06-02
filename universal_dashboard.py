# create_standalone_app.py
"""
Creates a standalone executable that users can run without Python installed
"""

import subprocess
import sys
import os

def create_standalone_app():
    """Create standalone executable for the dashboard"""
    
    print("🔧 Creating standalone app...")
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create the executable
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "ProjectReviewDashboard",
        "--add-data", "requirements.txt;.",
        "--hidden-import", "streamlit",
        "--hidden-import", "plotly",
        "--hidden-import", "pandas",
        "dashboard.py"
    ]
    
    subprocess.run(command)
    
    print("✅ Standalone app created in 'dist' folder!")
    print("📦 Users can now run 'ProjectReviewDashboard.exe' directly")

if __name__ == "__main__":
    create_standalone_app()

# Alternative: Auto-opening browser version
def create_auto_browser_version():
    """Creates version that automatically opens browser"""
    
    # Create launcher script
    launcher_code = '''
import webbrowser
import subprocess
import time
import threading

def run_dashboard():
    subprocess.run(["streamlit", "run", "dashboard.py", "--server.headless", "true"])

def open_browser():
    time.sleep(3)  # Wait for server to start
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    # Start dashboard in background
    dashboard_thread = threading.Thread(target=run_dashboard)
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    # Open browser
    open_browser()
    
    # Keep running
    input("Press Enter to exit...")
'''
    
    with open("run_dashboard.py", "w") as f:
        f.write(launcher_code)
    
    print("✅ Created 'run_dashboard.py' - double-click to start!")
