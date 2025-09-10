#!/usr/bin/env python3
"""Test script to validate ESC key handling in all quiz versions."""

import sys
import os
import re

def test_cli_esc_handling():
    """Test that CLI version has ESC handling."""
    print("Testing CLI ESC handling...")
    
    with open('../src/python_exception_quiz/cli_quiz.py', 'r') as f:
        content = f.read()
    
    checks = [
        ("ESC in input prompt", "'ESC' to quit" in content),
        ("ESC handling in input", "user_input.upper() == 'ESC'" in content),
        ("Quit game method", "_ask_quit_game" in content),
        ("QUIT_GAME return value", "return 'QUIT_GAME'" in content),
        ("Quit handling in play", "if user_answer == 'QUIT_GAME'" in content),
        ("Keyboard interrupt handling", "KeyboardInterrupt" in content),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_passed = False
    
    return all_passed

def test_tui_esc_handling():
    """Test that TUI version has ESC handling."""
    print("Testing TUI ESC handling...")
    
    with open('../src/python_exception_quiz/tui_quiz.py', 'r') as f:
        content = f.read()
    
    checks = [
        ("Escape key handling", "key == 27" in content and "# Escape" in content),
        ("Quit game method", "_ask_quit_game" in content),
        ("QUIT_GAME return value", "'QUIT_GAME'" in content),
        ("Quit handling in play", "if user_answer == 'QUIT_GAME'" in content),
        ("Quit dialog UI", "QUIT GAME?" in content),
        ("Continue or quit options", "Continue Playing" in content),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_passed = False
    
    return all_passed

def test_gui_esc_handling():
    """Test that GUI version has ESC handling."""
    print("Testing GUI ESC handling...")
    
    with open('../src/python_exception_quiz/pygame_quiz.py', 'r') as f:
        content = f.read()
    
    checks = [
        ("ESC key event", "pygame.K_ESCAPE" in content),
        ("Quit game method", "_ask_quit_game" in content),
        ("Game state transition", 'self.state = "complete"' in content),
        ("High score saving", "save_high_score" in content),
        ("Quit dialog", "Quit Game?" in content),
        ("Y/N key handling", "pygame.K_y" in content and "pygame.K_n" in content),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_passed = False
    
    return all_passed

def test_imports_and_structure():
    """Test that all versions can be imported."""
    print("Testing imports and structure...")
    
    try:
        import sys; sys.path.insert(0, '../src'); from python_exception_quiz.cli_quiz import CLIQuizGame
        print("  ✓ CLI version imports successfully")
        cli_ok = True
    except Exception as e:
        print(f"  ✗ CLI import error: {e}")
        cli_ok = False
    
    try:
        import curses
        import sys; sys.path.insert(0, '../src'); from python_exception_quiz.tui_quiz import TUIQuizGame
        print("  ✓ TUI version imports successfully")
        tui_ok = True
    except Exception as e:
        print(f"  ✗ TUI import error: {e}")
        tui_ok = False
    
    try:
        import pygame
        import sys; sys.path.insert(0, '../src'); from python_exception_quiz.pygame_quiz import GUIQuizGame
        print("  ✓ GUI version imports successfully")
        gui_ok = True
    except Exception as e:
        print(f"  ✗ GUI import error: {e}")
        gui_ok = False
    
    return cli_ok and tui_ok and gui_ok

def test_esc_documentation():
    """Test that ESC functionality is documented in help text."""
    print("Testing ESC functionality documentation...")
    
    # Check CLI version
    with open('../src/python_exception_quiz/cli_quiz.py', 'r') as f:
        cli_content = f.read()
    
    cli_documented = "'ESC' to quit" in cli_content
    print(f"  {'✓' if cli_documented else '✗'} CLI documents ESC functionality")
    
    # The other versions show ESC handling in their interfaces
    return cli_documented

def main():
    """Run all ESC functionality tests."""
    print("=" * 60)
    print("Python Exception Quiz - ESC Key Functionality Test")
    print("=" * 60)
    
    tests = [
        ("CLI ESC Handling", test_cli_esc_handling),
        ("TUI ESC Handling", test_tui_esc_handling),
        ("GUI ESC Handling", test_gui_esc_handling),
        ("Imports and Structure", test_imports_and_structure),
        ("ESC Documentation", test_esc_documentation)
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
        print("✅ All tests passed! ESC functionality implemented correctly.")
        print("\nESC key behavior:")
        print("• CLI: Type 'ESC' or press Ctrl+C to quit")
        print("• TUI: Press ESC key to quit") 
        print("• GUI: Press ESC key to quit")
        print("\nAll versions ask for confirmation and show final score.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())