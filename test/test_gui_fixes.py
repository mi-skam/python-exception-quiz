#!/usr/bin/env python3
"""Test script to validate GUI fixes work correctly."""

import sys
import os

def test_color_fixes():
    """Test that all color references are valid."""
    print("Testing color references...")
    
    # Read the GUI file
    with open('pygame_quiz.py', 'r') as f:
        content = f.read()
    
    # Define expected colors from COLORS dictionary
    valid_colors = {
        'background', 'surface', 'primary', 'secondary', 'success', 
        'error', 'warning', 'text', 'text_dim', 'border', 
        'input_bg', 'input_active'
    }
    
    # Find all COLORS references
    import re
    color_refs = re.findall(r"COLORS\['(\w+)'\]", content)
    
    issues = []
    for color_ref in set(color_refs):
        if color_ref not in valid_colors:
            issues.append(f"Invalid color reference: COLORS['{color_ref}']")
    
    if issues:
        for issue in issues:
            print(f"✗ {issue}")
        return False
    else:
        print(f"✓ All {len(set(color_refs))} color references are valid")
        return True

def test_code_split_fixes():
    """Test that code splitting is fixed."""
    print("Testing code split fixes...")
    
    # Read the GUI file
    with open('pygame_quiz.py', 'r') as f:
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

def test_pygame_imports():
    """Test that pygame can be imported and GUI structure exists."""
    print("Testing pygame imports and structure...")
    
    try:
        import pygame
        import pygame.freetype
        print("✓ pygame and pygame.freetype available")
    except ImportError as e:
        print(f"✗ pygame import error: {e}")
        return False
    
    try:
        from pygame_quiz import GUIQuizGame, Button, InputBox
        print("✓ GUI classes can be imported")
        
        # Test that GUIQuizGame is callable
        if callable(GUIQuizGame):
            print("✓ GUIQuizGame class is callable")
        else:
            print("✗ GUIQuizGame class is not callable")
            return False
            
        return True
    except Exception as e:
        print(f"✗ GUI import error: {e}")
        return False

def test_color_definitions():
    """Test that the COLORS dictionary has all needed colors."""
    print("Testing color definitions...")
    
    try:
        from pygame_quiz import COLORS
        
        expected_colors = [
            'background', 'surface', 'primary', 'secondary', 'success', 
            'error', 'warning', 'text', 'text_dim', 'border', 
            'input_bg', 'input_active'
        ]
        
        missing_colors = []
        for color in expected_colors:
            if color not in COLORS:
                missing_colors.append(color)
        
        if missing_colors:
            print(f"✗ Missing colors: {missing_colors}")
            return False
        else:
            print(f"✓ All {len(expected_colors)} required colors defined")
            
        # Check that colors are RGB tuples
        for color_name, color_value in COLORS.items():
            if not (isinstance(color_value, tuple) and len(color_value) == 3):
                print(f"✗ Invalid color format for {color_name}: {color_value}")
                return False
            
            if not all(0 <= c <= 255 for c in color_value):
                print(f"✗ Invalid color values for {color_name}: {color_value}")
                return False
        
        print("✓ All colors have valid RGB format")
        return True
        
    except Exception as e:
        print(f"✗ Color definition error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Python Exception Quiz - GUI Bug Fix Validation")
    print("=" * 60)
    
    tests = [
        test_color_fixes,
        test_code_split_fixes,
        test_pygame_imports,
        test_color_definitions
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
        print("✅ All tests passed! GUI 'info' color bug has been fixed.")
        print("\nThe GUI should now work correctly:")
        print("  uv run quiz.py gui")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())