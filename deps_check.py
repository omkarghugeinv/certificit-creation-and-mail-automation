import sys
import subprocess

def ensure_dependencies():
    required_packages = {'Pillow': 'PIL', 'reportlab': 'reportlab', 'pypdf': 'pypdf'}
    missing = []
    for package, module in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
            print("Dependencies installed successfully.")
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            print("Please manually run: pip install -r requirements.txt")
            sys.exit(1)
