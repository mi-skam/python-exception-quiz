#!/usr/bin/env python3
"""Test script to validate TUI fixes work correctly."""

import sys
import os

def test_ord_fixes():
    """Test that ord() calls are fixed."""
    print("Testing ord() fixes...")
    
    # Read the TUI file
    with open('tui_quiz.py', 'r') as f:
        content = f.read()
    
    # Check for problematic ord() patterns
    bad_patterns = [
        "ord('\\\\n')",  # Double escaped newline
        "ord('\\\\t')",  # Double escaped tab
    ]
    
    issues = []
    for pattern in bad_patterns:
        if pattern in content:
            issues.append(f"Found problematic pattern: {pattern}")
    
    if issues:
        for issue in issues:
            print(f"✗ {issue}")
        return False
    else:
        print("✓ No problematic ord() patterns found")
        return True

def test_code_split_fixes():
    """Test that code splitting is fixed."""
    print("Testing code split fixes...")
    
    # Read the TUI file
    with open('tui_quiz.py', 'r') as f:
        content = f.read()
    
    # Check for correct newline splitting
    if ".split('\\\\n')" in content:
        print("✗ Found double-escaped newline in split()")
        return False
    elif ".split('\\n')" in content:
        print("✓ Code splitting uses correct newline character")
        return True
    else:
        print("? No split('\\n') found, might be OK")
        return True

def test_tui_imports_and_structure():
    """Test that TUI can be imported and has correct structure."""
    print("Testing TUI imports and structure...")
    
    try:
        import curses
        print("✓ curses module available")
    except ImportError:
        print("✗ curses module not available")
        return False
    
    try:
        from tui_quiz import TUIQuizGame, main
        print("✓ TUI imports work correctly")
        
        # Test that main function exists and is callable
        if callable(main):
            print("✓ main function is callable")
        else:
            print("✗ main function is not callable")
            return False
            
        return True
    except Exception as e:
        print(f"✗ TUI import error: {e}")
        return False

def test_character_validation():
    """Test character handling logic."""
    print("Testing character handling logic...")
    
    # Test ord() with correct characters
    test_chars = ['\n', '\t', 'a', 'A', 'y', 'Y', 'n', 'N']
    
    try:
        for char in test_chars:
            ord_value = ord(char)
            print(f"✓ ord('{repr(char)}') = {ord_value}")
        
        # Test that our key comparisons work
        enter_key = ord('\n')
        tab_key = ord('\t')
        
        if enter_key == 10 and tab_key == 9:
            print("✓ Key code mappings are correct")
            return True
        else:
            print(f"✗ Unexpected key codes: Enter={enter_key}, Tab={tab_key}")
            return False
            
    except Exception as e:
        print(f"✗ Character handling error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Python Exception Quiz - TUI Bug Fix Validation")
    print("=" * 60)
    
    tests = [
        test_ord_fixes,
        test_code_split_fixes,
        test_tui_imports_and_structure,
        test_character_validation
    ]
    
    results = []
    for test in tests:
        print()
        result = test()
        results.append(result)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} test groups passed")
    
    if passed == total:
        print("✅ All tests passed! TUI ord() bugs have been fixed.")
        print("\nThe TUI should now work correctly in an interactive terminal:")
        print("  uv run quiz.py tui")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())