#!/usr/bin/env python3
"""
Build script for creating executable versions of the Python Exception Quiz
Supports Windows, macOS, and Linux builds using PyInstaller
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def build_executable(platform="auto"):
    """Build executable for the specified platform."""
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Platform-specific settings
    if platform == "auto":
        import platform as plt
        current_os = plt.system().lower()
        if current_os == "darwin":
            platform = "macos"
        elif current_os == "windows":
            platform = "windows"
        else:
            platform = "linux"
    
    print(f"Building for platform: {platform}")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable
        "--windowed",                   # No console window
        "--name", "PythonExceptionQuiz", # Executable name
        "--hidden-import", "pygame",    # Ensure pygame is included
        "--hidden-import", "pygame.freetype",
        "--hidden-import", "curses",    # For TUI support
        "--hidden-import", "sqlite3",   # For database
        "--hidden-import", "json",      # For data files
    ]
    
    # Add icon if it exists
    if os.path.exists("data/icon.ico"):
        cmd.extend(["--icon", "data/icon.ico"])
    
    # Add data directories
    cmd.extend([
        "--add-data", "data:data",      # Include data directory
        "--add-data", "src:src",        # Include source directory
        "quiz.py"                       # Use quiz.py as main entry point
    ])
    
    print(f"Building executable with command: {' '.join(cmd)}")
    
    try:
        # Use uv run to ensure we're using the correct environment
        uv_cmd = ["uv", "run"] + cmd
        subprocess.check_call(uv_cmd)
        print("\nBuild successful!")
        
        # List the created files
        dist_path = Path("dist")
        if dist_path.exists():
            print("\nCreated files:")
            for file in dist_path.iterdir():
                size = file.stat().st_size / (1024 * 1024)  # MB
                print(f"  - {file.name} ({size:.1f} MB)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False

def create_dist_package():
    """Create a distribution package with the executable and assets."""
    # Look for executable with or without .exe extension
    exe_path = None
    if os.path.exists("dist/PythonExceptionQuiz.exe"):
        exe_path = "dist/PythonExceptionQuiz.exe"
        exe_name = "PythonExceptionQuiz.exe"
    elif os.path.exists("dist/PythonExceptionQuiz"):
        exe_path = "dist/PythonExceptionQuiz"
        exe_name = "PythonExceptionQuiz"
    
    if not exe_path:
        print("Executable not found. Run build first.")
        return False
    
    # Create package directory
    package_dir = "dist/PythonExceptionQuiz_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # Copy executable
    shutil.copy(exe_path, f"{package_dir}/{exe_name}")
    
    # Copy data files if they exist
    if os.path.exists("data"):
        shutil.copytree("data", f"{package_dir}/data")
    
    # Create README for distribution
    readme_content = """# Python Exception Quiz

A fun and educational quiz game to learn Python exception handling!

## How to Play

1. Double-click `PythonExceptionQuiz` to start the game
2. View Python code snippets and identify which exception will be raised
3. Type your answer and press Enter
4. Progress through levels: Simple → Intermediate → Expert
5. Compete for high scores!

## Controls

- Type exception names (e.g., "ValueError", "TypeError")
- Use arrow keys or Tab for autocomplete suggestions
- Mouse wheel to scroll through long code samples
- ESC to quit current game (progress is saved)

## System Requirements

- Works on Windows, macOS, and Linux
- No Python installation required - everything is included!

Enjoy learning Python exceptions!
"""
    
    with open(f"{package_dir}/README.txt", "w") as f:
        f.write(readme_content)
    
    print(f"Distribution package created: {package_dir}/")
    return True

def main():
    """Main build script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Python Exception Quiz executable")
    parser.add_argument("--platform", choices=["windows", "macos", "linux", "auto"], 
                       default="auto", help="Target platform (default: auto-detect)")
    parser.add_argument("--package", action="store_true", 
                       help="Create distribution package")
    
    args = parser.parse_args()
    
    print("Building Python Exception Quiz executable...")
    
    if build_executable(args.platform):
        if args.package:
            create_dist_package()
        
        print("\nReady for itch.io upload!")
        print("Upload the files in the 'dist/' directory to itch.io as a downloadable game.")
    else:
        print("\nBuild failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()