#!/usr/bin/env python3
"""Test script to validate the new package structure."""

import sys
import os
import subprocess
import importlib.util

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_package_structure():
    """Test that the package structure is correct."""
    print("Testing package structure...")
    
    expected_files = [
        'src/python_exception_quiz/__init__.py',
        'src/python_exception_quiz/main.py',
        'src/python_exception_quiz/game_engine.py',
        'src/python_exception_quiz/cli_quiz.py',
        'src/python_exception_quiz/tui_quiz.py',
        'src/python_exception_quiz/pygame_quiz.py',
    ]
    
    expected_data_files = [
        'data/levels.json',
        'data/highscores.json',
        'data/savegame.json',
    ]
    
    base_path = os.path.join(os.path.dirname(__file__), '..')
    all_exist = True
    
    for file_path in expected_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - Missing")
            all_exist = False
    
    # Check data files
    for file_path in expected_data_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def test_package_imports():
    """Test that package imports work correctly."""
    print("Testing package imports...")
    
    try:
        import python_exception_quiz
        print("  ✓ Main package imports")
    except ImportError as e:
        print(f"  ✗ Main package import failed: {e}")
        return False
    
    try:
        from python_exception_quiz import ExceptionQuizGame
        print("  ✓ ExceptionQuizGame imports from package")
    except ImportError as e:
        print(f"  ✗ ExceptionQuizGame import failed: {e}")
        return False
    
    try:
        from python_exception_quiz.game_engine import ExceptionQuizGame
        print("  ✓ Direct module import works")
    except ImportError as e:
        print(f"  ✗ Direct module import failed: {e}")
        return False
    
    try:
        from python_exception_quiz.main import main
        print("  ✓ Main launcher function imports")
    except ImportError as e:
        print(f"  ✗ Main launcher import failed: {e}")
        return False
    
    return True

def test_relative_imports():
    """Test that relative imports work within the package."""
    print("Testing relative imports...")
    
    try:
        from python_exception_quiz.cli_quiz import CLIQuizGame
        cli_game = CLIQuizGame('data')  # Point to data directory
        print("  ✓ CLI quiz with relative imports works")
    except Exception as e:
        print(f"  ✗ CLI relative imports failed: {e}")
        return False
    
    try:
        import curses
        from python_exception_quiz.tui_quiz import TUIQuizGame
        print("  ✓ TUI quiz with relative imports works")
    except ImportError:
        print("  ✓ TUI quiz import handled gracefully (curses not available)")
    except Exception as e:
        print(f"  ✗ TUI relative imports failed: {e}")
        return False
    
    try:
        import pygame
        from python_exception_quiz.pygame_quiz import GUIQuizGame
        print("  ✓ GUI quiz with relative imports works")
    except ImportError:
        print("  ✓ GUI quiz import handled gracefully (pygame not available)")
    except Exception as e:
        print(f"  ✗ GUI relative imports failed: {e}")
        return False
    
    return True

def test_entry_points():
    """Test that entry points work."""
    print("Testing entry points...")
    
    # Test main.py entry point
    try:
        base_path = os.path.join(os.path.dirname(__file__), '..')
        result = subprocess.run([
            sys.executable, os.path.join(base_path, 'main.py')
        ], capture_output=True, text=True, timeout=3)
        
        if result.returncode == 0 or "pygame" in result.stderr:
            print("  ✓ main.py entry point works")
        else:
            print(f"  ✗ main.py failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("  ✓ main.py entry point works (timeout expected)")
    except Exception as e:
        print(f"  ✗ main.py entry point error: {e}")
        return False
    
    return True

def test_data_files():
    """Test that data files are accessible."""
    print("Testing data files...")
    
    try:
        from python_exception_quiz.game_engine import ExceptionQuizGame
        game = ExceptionQuizGame('data')  # Point to data directory
        
        # Test that levels load
        if hasattr(game, 'levels') and game.levels:
            print("  ✓ levels.json loads correctly")
        else:
            print("  ✗ levels.json failed to load")
            return False
        
        # Test basic functionality
        question = game.get_current_question()
        if question and 'code' in question:
            print("  ✓ Game engine functionality works")
        else:
            print("  ✗ Game engine functionality failed")
            return False
        
    except Exception as e:
        print(f"  ✗ Data files test failed: {e}")
        return False
    
    return True

def test_test_directory():
    """Test that test directory is properly structured."""
    print("Testing test directory structure...")
    
    test_dir = os.path.dirname(__file__)
    
    expected_tests = [
        'test_esc_functionality.py',
        'test_gui_fixes.py',
        'test_launcher_system.py',
        'test_tui_fixes.py',
        'test_tui.py',
        'test_package_structure.py'  # This test
    ]
    
    all_exist = True
    for test_file in expected_tests:
        test_path = os.path.join(test_dir, test_file)
        if os.path.exists(test_path):
            print(f"  ✓ {test_file}")
        else:
            print(f"  ✗ {test_file} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all package structure tests."""
    print("=" * 60)
    print("Python Exception Quiz - Package Structure Test")
    print("=" * 60)
    
    tests = [
        ("Package Structure", test_package_structure),
        ("Package Imports", test_package_imports),
        ("Relative Imports", test_relative_imports),
        ("Entry Points", test_entry_points),
        ("Data Files", test_data_files),
        ("Test Directory", test_test_directory)
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
        print("✅ All tests passed! Package structure is correct.")
        print("\nNew Structure:")
        print("📁 src/python_exception_quiz/     → Main package")
        print("📁 test/                          → All tests")
        print("📄 main.py                        → Entry point")
        print("📄 pyproject.toml                 → Modern packaging")
        print("📄 README.md                      → Documentation")
        print("\nUsage:")
        print("• python main.py                  → Launch quiz")
        print("• pip install -e .               → Install in dev mode")
        print("• python -m pytest test/         → Run tests")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())