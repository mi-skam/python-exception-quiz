#!/usr/bin/env python3
"""
Build script for creating web version of the Python Exception Quiz
Uses pygbag to convert pygame to browser-compatible WebAssembly
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def install_pygbag():
    """Install pygbag if not already available."""
    try:
        import pygbag
        print("pygbag is already installed")
    except ImportError:
        print("Installing pygbag...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])

def prepare_web_build():
    """Prepare the project structure for web build."""
    
    # Create web build directory
    web_dir = Path("web_build")
    if web_dir.exists():
        shutil.rmtree(web_dir)
    web_dir.mkdir()
    
    # Copy necessary files
    files_to_copy = [
        "pygame_web.py",
        "src/",
        "data/" if os.path.exists("data") else None,
        "levels.json" if os.path.exists("levels.json") else None
    ]
    
    for file_path in files_to_copy:
        if file_path and os.path.exists(file_path):
            if os.path.isfile(file_path):
                shutil.copy2(file_path, web_dir / Path(file_path).name)
            else:
                shutil.copytree(file_path, web_dir / Path(file_path).name)
    
    # Create a simple main.py for pygbag
    main_content = '''#!/usr/bin/env python3
"""
Main entry point for web version of Python Exception Quiz
"""
import asyncio
import sys
import os

# Add current directory to path to find modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pygame_web import main

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open(web_dir / "main.py", "w") as f:
        f.write(main_content)
    
    return web_dir

def build_web():
    """Build the web version using pygbag."""
    
    # Install pygbag
    install_pygbag()
    
    # Prepare build
    web_dir = prepare_web_build()
    
    # Change to web build directory
    original_dir = os.getcwd()
    os.chdir(web_dir)
    
    try:
        # Build with pygbag
        cmd = [
            sys.executable, "-m", "pygbag",
            "--width", "800",
            "--height", "600", 
            "--name", "Python Exception Quiz",
            "--icon", "icon.ico" if os.path.exists("icon.ico") else "",
            "main.py"
        ]
        
        # Remove empty arguments
        cmd = [arg for arg in cmd if arg]
        
        print(f"Building web version with command: {' '.join(cmd)}")
        
        subprocess.check_call(cmd)
        
        print("\n✅ Web build successful!")
        
        # Copy built files back to main directory
        dist_web = Path(original_dir) / "dist_web"
        if dist_web.exists():
            shutil.rmtree(dist_web)
        
        # Find the generated files
        for item in Path(".").iterdir():
            if item.is_dir() and "dist" in item.name.lower():
                shutil.copytree(item, dist_web)
                break
        else:
            # Copy all HTML/JS files as fallback
            dist_web.mkdir(exist_ok=True)
            for ext in ["*.html", "*.js", "*.wasm", "*.data"]:
                for file in Path(".").glob(ext):
                    shutil.copy2(file, dist_web)
        
        print(f"Web files copied to: {dist_web}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Web build failed with error: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

def create_itch_package():
    """Create an itch.io-ready package for web deployment."""
    
    dist_web = Path("dist_web")
    if not dist_web.exists():
        print("❌ Web build not found. Run build first.")
        return False
    
    # Create itch package
    itch_dir = Path("itch_web_package")
    if itch_dir.exists():
        shutil.rmtree(itch_dir)
    
    # Copy web files
    shutil.copytree(dist_web, itch_dir)
    
    # Create index.html if it doesn't exist
    index_path = itch_dir / "index.html"
    if not index_path.exists():
        # Create a basic index.html
        index_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Python Exception Quiz</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1e1e2e;
            color: #f0f0f5;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        #gameContainer {
            border: 2px solid #646480;
            border-radius: 8px;
            padding: 10px;
            background-color: #2a2a40;
        }
        
        canvas {
            display: block;
            image-rendering: pixelated;
        }
        
        .info {
            margin: 10px 0;
            text-align: center;
        }
        
        .controls {
            margin-top: 15px;
            font-size: 14px;
            color: #b0b0c0;
            text-align: center;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <h1>🐍 Python Exception Quiz 🐍</h1>
    <p class="info">Learn Python exception handling through interactive gameplay!</p>
    
    <div id="gameContainer">
        <canvas id="canvas" width="800" height="600"></canvas>
    </div>
    
    <div class="controls">
        <strong>How to Play:</strong><br>
        • View Python code snippets and identify which exception will be raised<br>
        • Type the exact exception name (e.g., "ValueError", "TypeError")<br>
        • Use Tab or arrow keys for autocomplete suggestions<br>
        • Progress through difficulty levels for higher scores!<br>
        <br>
        <em>Click on the game area to start playing. Have fun learning! 🎮</em>
    </div>
    
    <script>
        // Basic pygame-web integration
        // This will be replaced by pygbag's generated code
        console.log("Python Exception Quiz - Web Version");
    </script>
</body>
</html>'''
        
        with open(index_path, "w") as f:
            f.write(index_content)
    
    print(f"✅ Itch.io web package created: {itch_dir}/")
    print("\nTo upload to itch.io:")
    print("1. Zip the contents of itch_web_package/")
    print("2. Upload to itch.io as HTML game")
    print("3. Set 'This file will be played in the browser' for index.html")
    print("4. Set viewport dimensions to 800x600 or larger")
    
    return True

def main():
    """Main build script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Python Exception Quiz for web")
    parser.add_argument("--package", action="store_true", 
                       help="Create itch.io package after build")
    
    args = parser.parse_args()
    
    print("🌐 Building Python Exception Quiz for web...")
    
    if build_web():
        if args.package:
            create_itch_package()
        
        print("\n📦 Web build ready!")
        print("Files are in dist_web/ directory")
        
        if args.package:
            print("Itch.io package is in itch_web_package/ directory")
    else:
        print("\n❌ Web build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()