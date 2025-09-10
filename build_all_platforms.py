#!/usr/bin/env python3
"""
Multi-platform build script for Python Exception Quiz
Creates executables for Windows, macOS, and Linux
"""

import subprocess
import sys
import os
import shutil
import platform
from pathlib import Path

def get_platform_info():
    """Get current platform information."""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    platform_map = {
        'darwin': 'macos',
        'windows': 'windows', 
        'linux': 'linux'
    }
    
    return platform_map.get(system, system), arch

def build_for_current_platform():
    """Build for the current platform using the existing build script."""
    print(f"🔨 Building for current platform...")
    
    try:
        result = subprocess.run([sys.executable, "build_executable.py", "--package"], 
                              check=True, capture_output=True, text=True)
        print("✅ Current platform build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Current platform build failed: {e}")
        print(f"Output: {e.output}")
        return False

def create_universal_package():
    """Create a universal package for distribution."""
    print("📦 Creating universal distribution package...")
    
    current_platform, arch = get_platform_info()
    
    # Create universal dist directory
    universal_dist = Path("dist_universal")
    if universal_dist.exists():
        shutil.rmtree(universal_dist)
    
    universal_dist.mkdir()
    
    # Copy current platform build
    if Path("dist/PythonExceptionQuiz_Package").exists():
        platform_dir = universal_dist / f"{current_platform}_{arch}"
        shutil.copytree("dist/PythonExceptionQuiz_Package", platform_dir)
        print(f"✅ Added {current_platform}_{arch} build")
    
    # Create README for multi-platform distribution
    readme_content = f"""# Python Exception Quiz - Multi-Platform Distribution

## Available Builds

### {current_platform.title()} ({arch})
- Directory: `{current_platform}_{arch}/`
- Run: `{current_platform}_{arch}/PythonExceptionQuiz{"" if current_platform != "windows" else ".exe"}`

## System Requirements

- **Windows**: Windows 10 or later, x64 architecture
- **macOS**: macOS 10.14 or later, Intel/Apple Silicon
- **Linux**: Most modern distributions with X11/Wayland

## Installation

1. Extract this archive
2. Navigate to your platform's directory  
3. Run the executable for your system
4. No additional installation required!

## Controls

- Type exception names (e.g., "ValueError", "TypeError")
- Use Tab or arrow keys for autocomplete
- Mouse wheel to scroll code samples
- ESC to quit (progress saved automatically)

## About

A fun and educational quiz game to test your knowledge of Python's exception hierarchy!

Generated with PyInstaller on {current_platform} {arch}
"""
    
    with open(universal_dist / "README.txt", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Universal package created: {universal_dist}/")
    return str(universal_dist)

def print_build_instructions():
    """Print instructions for building on other platforms."""
    current_platform, arch = get_platform_info()
    
    print("\n" + "="*60)
    print("🚀 MULTI-PLATFORM BUILD INSTRUCTIONS")
    print("="*60)
    
    print(f"\n✅ Current platform ({current_platform} {arch}) build completed!")
    
    print("\n📋 To build for other platforms:")
    
    if current_platform != "windows":
        print("\n🪟 Windows:")
        print("  1. Set up Windows machine/VM with Python 3.8+")
        print("  2. Install uv: pip install uv")
        print("  3. Clone repository and cd to project directory")
        print("  4. Run: uv sync")
        print("  5. Run: python build_executable.py --package")
        print("  6. Upload dist/PythonExceptionQuiz_Package/ to itch.io")
    
    if current_platform != "linux":
        print("\n🐧 Linux:")
        print("  1. Set up Linux machine/container with Python 3.8+")
        print("  2. Install system dependencies: apt-get install python3-dev")
        print("  3. Install uv: pip install uv") 
        print("  4. Clone repository and cd to project directory")
        print("  5. Run: uv sync")
        print("  6. Run: python build_executable.py --package")
        print("  7. Upload dist/PythonExceptionQuiz_Package/ to itch.io")
    
    print("\n🎯 Alternative Options:")
    print("  • GitHub Actions CI/CD for automated multi-platform builds")
    print("  • Docker containers for consistent build environments")
    print("  • Cloud build services (AWS CodeBuild, etc.)")
    
    print("\n📦 For itch.io:")
    print("  • Upload each platform's package separately")
    print("  • Or create one package with all platforms included")
    print("  • Mark appropriate platform compatibility for each")

def main():
    """Main build orchestration."""
    print("🎮 Python Exception Quiz - Multi-Platform Builder")
    print("="*50)
    
    # Build for current platform
    if not build_for_current_platform():
        print("\n❌ Build failed!")
        sys.exit(1)
    
    # Create universal package
    universal_path = create_universal_package()
    
    # Print instructions
    print_build_instructions()
    
    print(f"\n📁 Build outputs:")
    print(f"  • Single platform: dist/PythonExceptionQuiz_Package/")
    print(f"  • Universal package: {universal_path}/")
    
    print(f"\n🎉 Ready for distribution!")

if __name__ == "__main__":
    main()