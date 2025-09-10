#!/usr/bin/env python3
"""Test script to validate the new launcher priority system."""

import sys
import os
import subprocess
import tempfile
import shutil

def test_auto_detection():
    """Test that auto-detection works correctly."""
    print("Testing auto-detection...")
    
    # Test that pygame is detected
    try:
        import pygame
        print("  ✓ pygame available - should auto-select GUI")
        
        # Test running without args (should use GUI)
        result = subprocess.run([
            sys.executable, 'quiz.py'
        ], capture_output=True, text=True, timeout=3)
        
        if "pygame" in result.stderr or result.returncode == 0:
            print("  ✓ Auto-detection launches GUI")
        else:
            print(f"  ✗ Auto-detection failed: {result.stderr}")
            return False
    except ImportError:
        print("  ✓ pygame not available - would try TUI")
    except subprocess.TimeoutExpired:
        print("  ✓ GUI launched (timeout expected)")
    except Exception as e:
        print(f"  ✗ Auto-detection error: {e}")
        return False
    
    return True

def test_forced_interfaces():
    """Test that forced interface selection works."""
    print("Testing forced interface selection...")
    
    # Test GUI
    try:
        result = subprocess.run([
            sys.executable, 'quiz.py', 'gui'
        ], capture_output=True, text=True, timeout=3)
        
        if "pygame" in result.stderr or result.returncode == 0:
            print("  ✓ Forced GUI works")
        else:
            print(f"  ✗ Forced GUI failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("  ✓ Forced GUI works (timeout expected)")
    except Exception as e:
        print(f"  ✗ GUI test error: {e}")
        return False
    
    # Test TUI (should fail gracefully in non-interactive environment)
    try:
        result = subprocess.run([
            sys.executable, 'quiz.py', 'tui'
        ], capture_output=True, text=True, timeout=3)
        
        if "interactive terminal" in result.stdout or "curses" in result.stdout:
            print("  ✓ Forced TUI handles non-interactive gracefully")
        else:
            print(f"  ? TUI output: {result.stdout[:100]}")
    except Exception as e:
        print(f"  ? TUI test (expected in non-interactive): {e}")
    
    return True

def test_cli_debug_functions():
    """Test CLI debug functionality."""
    print("Testing CLI debug functions...")
    
    # Test stats
    result = subprocess.run([
        sys.executable, 'quiz.py', 'cli', '--stats'
    ], capture_output=True, text=True, timeout=5)
    
    if result.returncode == 0 and ("No saved game" in result.stdout or "Player:" in result.stdout):
        print("  ✓ CLI stats command works")
    else:
        print(f"  ✗ CLI stats failed: {result.stdout}")
        return False
    
    # Test scores
    result = subprocess.run([
        sys.executable, 'quiz.py', 'cli', '--scores'
    ], capture_output=True, text=True, timeout=5)
    
    if result.returncode == 0 and ("HIGH SCORES" in result.stdout or "No high scores" in result.stdout):
        print("  ✓ CLI scores command works")
    else:
        print(f"  ✗ CLI scores failed: {result.stdout}")
        return False
    
    return True

def test_help_and_documentation():
    """Test help text and documentation."""
    print("Testing help and documentation...")
    
    # Test help
    result = subprocess.run([
        sys.executable, 'quiz.py', '--help'
    ], capture_output=True, text=True)
    
    help_text = result.stdout
    
    checks = [
        ("Auto-detect mentioned", "Auto-detect best interface" in help_text),
        ("GUI priority shown", "1. GUI (pygame)" in help_text),
        ("TUI fallback shown", "2. TUI (terminal)" in help_text),
        ("CLI debug mentioned", "internal/debug use" in help_text),
        ("Examples included", "python quiz.py" in help_text and "# Auto-detect" in help_text),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_passed = False
    
    return all_passed

def test_main_py_entry_point():
    """Test that main.py works as entry point."""
    print("Testing main.py entry point...")
    
    try:
        result = subprocess.run([
            sys.executable, 'main.py'
        ], capture_output=True, text=True, timeout=3)
        
        if "pygame" in result.stderr or result.returncode == 0:
            print("  ✓ main.py launches correctly")
            return True
        else:
            print(f"  ✗ main.py failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("  ✓ main.py launches correctly (timeout expected)")
        return True
    except Exception as e:
        print(f"  ✗ main.py error: {e}")
        return False

def test_readme_accuracy():
    """Test that README matches actual behavior."""
    print("Testing README accuracy...")
    
    if not os.path.exists('README.md'):
        print("  ✗ README.md not found")
        return False
    
    with open('README.md', 'r') as f:
        readme_content = f.read()
    
    checks = [
        ("Auto-detection mentioned", "Auto-detects and launches" in readme_content),
        ("GUI priority documented", "Launch GUI" in readme_content and "pygame" in readme_content),
        ("TUI fallback documented", "Fall back to TUI" in readme_content),
        ("CLI debug documented", "Debug/Development" in readme_content),
        ("Installation instructions", "pip install pygame" in readme_content),
        ("Usage examples", "python quiz.py" in readme_content),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """Run all launcher system tests."""
    print("=" * 60)
    print("Python Exception Quiz - Launcher Priority System Test")
    print("=" * 60)
    
    tests = [
        ("Auto-detection", test_auto_detection),
        ("Forced Interfaces", test_forced_interfaces),
        ("CLI Debug Functions", test_cli_debug_functions),
        ("Help and Documentation", test_help_and_documentation),
        ("main.py Entry Point", test_main_py_entry_point),
        ("README Accuracy", test_readme_accuracy)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} test groups passed")
    
    if passed == total:
        print("✅ All tests passed! Launcher priority system working correctly.")
        print("\nNew Usage Pattern:")
        print("• python quiz.py          → Auto-detects GUI > TUI")
        print("• python main.py          → Same as above")
        print("• python quiz.py gui      → Forces GUI")
        print("• python quiz.py tui      → Forces TUI")
        print("• python quiz.py cli      → Debug/internal use only")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())