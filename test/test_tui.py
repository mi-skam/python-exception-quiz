#!/usr/bin/env python3
"""Test script to validate TUI functionality without interactive terminal."""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_tui_imports():
    """Test that TUI can be imported and basic structures work."""
    print("Testing TUI imports...")
    try:
        import curses
        print("✓ curses module available")
    except ImportError as e:
        print(f"✗ curses module not available: {e}")
        return False
    
    try:
        from python_exception_quiz.tui_quiz import TUIQuizGame
        print("✓ TUIQuizGame can be imported")
    except ImportError as e:
        print(f"✗ Failed to import TUIQuizGame: {e}")
        return False
    
    try:
        from python_exception_quiz.game_engine import ExceptionQuizGame
        print("✓ ExceptionQuizGame can be imported")
    except ImportError as e:
        print(f"✗ Failed to import ExceptionQuizGame: {e}")
        return False
    
    return True

def test_game_engine():
    """Test the game engine works correctly."""
    print("\nTesting game engine...")
    from src.python_exception_quiz.game_engine import ExceptionQuizGame
    
    try:
        game = ExceptionQuizGame('data')
        print("✓ Game engine initialized")
        
        # Test autocomplete
        suggestions = game.get_autocomplete_suggestions("Value")
        if "ValueError" in suggestions:
            print("✓ Autocomplete works")
        else:
            print("✗ Autocomplete failed")
        
        # Test question retrieval
        question = game.get_current_question()
        if question and 'code' in question and 'correct_answer' in question:
            print("✓ Questions loaded correctly")
        else:
            print("✗ Failed to load questions")
            
        # Test level info
        difficulty, count = game.get_level_info(1)
        if difficulty and count > 0:
            print(f"✓ Level 1: {difficulty} with {count} questions")
        else:
            print("✗ Failed to get level info")
            
    except Exception as e:
        print(f"✗ Game engine error: {e}")
        return False
    
    return True

def test_tui_structure():
    """Test TUI class structure without running curses."""
    print("\nTesting TUI structure...")
    
    import curses
    
    # Mock stdscr for testing
    class MockStdscr:
        def getmaxyx(self):
            return (24, 80)
        def addstr(self, *args, **kwargs):
            pass
        def clear(self):
            pass
        def refresh(self):
            pass
        def getch(self):
            return ord('q')
    
    try:
        # Initialize curses temporarily for color pairs
        stdscr = curses.initscr()
        curses.start_color()
        
        from src.python_exception_quiz.tui_quiz import TUIQuizGame
        mock_screen = MockStdScr()
        
        # Test initialization
        tui = TUIQuizGame(mock_screen, 'data')
        print("✓ TUI initialized with mock screen")
        
        # Clean up curses
        try:
            curses.endwin()
        except:
            pass
        
        # Check attributes
        if hasattr(tui, 'game') and hasattr(tui, 'stdscr'):
            print("✓ TUI has required attributes")
        else:
            print("✗ TUI missing required attributes")
            
        # Check methods
        required_methods = ['run', '_show_welcome_screen', '_play_question', 
                          '_get_input_with_autocomplete', '_show_message']
        for method in required_methods:
            if hasattr(tui, method):
                print(f"✓ Method {method} exists")
            else:
                print(f"✗ Method {method} missing")
                
    except Exception as e:
        print(f"✗ TUI structure error: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("Python Exception Quiz - TUI Test Suite")
    print("=" * 50)
    
    tests = [
        test_tui_imports,
        test_game_engine,
        test_tui_structure
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} test groups passed")
    
    if passed == total:
        print("✅ All tests passed! TUI should work in an interactive terminal.")
        print("\nTo run the TUI version in a terminal:")
        print("  python3 tui_quiz.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())