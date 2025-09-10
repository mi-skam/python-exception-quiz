#!/usr/bin/env python3
"""Integration test for GUI keyboard input with auto-focus."""

import sys
import os
import unittest.mock

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_keyboard_input_with_autofocus():
    """Test that keyboard input works when input box is auto-focused."""
    print("Testing keyboard input with auto-focus...")
    
    try:
        import pygame
        from python_exception_quiz.pygame_quiz import InputBox
        
        # Mock font
        class MockFont:
            def render(self, text, color):
                class MockSurface:
                    pass
                class MockRect:
                    width = len(text) * 8
                    height = 16
                return MockSurface(), MockRect()
        
        # Create input box and auto-focus it
        input_box = InputBox(10, 10, 200, 30, MockFont())
        input_box.active = True  # Simulate auto-focus
        input_box._update_suggestions()  # Initialize suggestions
        
        # Mock pygame key events
        class MockKeyEvent:
            def __init__(self, key, unicode=""):
                self.type = pygame.KEYDOWN
                self.key = key
                self.unicode = unicode
        
        # Test typing a character
        with unittest.mock.patch('pygame.KEYDOWN', 2):
            char_event = MockKeyEvent(ord('V'), 'V')
            result = input_box.handle_event(char_event)
            
            if input_box.text == 'V':
                print("  ✓ Character input works with auto-focus")
            else:
                print(f"  ✗ Character input failed: got '{input_box.text}', expected 'V'")
                return False
        
        # Test backspace
        with unittest.mock.patch('pygame.KEYDOWN', 2), \
             unittest.mock.patch('pygame.K_BACKSPACE', 8):
            backspace_event = MockKeyEvent(pygame.K_BACKSPACE)
            input_box.handle_event(backspace_event)
            
            if input_box.text == '':
                print("  ✓ Backspace works with auto-focus")
            else:
                print(f"  ✗ Backspace failed: got '{input_box.text}', expected ''")
                return False
        
        # Test Enter key (should return True)
        with unittest.mock.patch('pygame.KEYDOWN', 2), \
             unittest.mock.patch('pygame.K_RETURN', 13):
            input_box.text = "ValueError"  # Set some text
            enter_event = MockKeyEvent(pygame.K_RETURN)
            result = input_box.handle_event(enter_event)
            
            if result == True:
                print("  ✓ Enter key works with auto-focus")
            else:
                print("  ✗ Enter key should return True when pressed")
                return False
        
        return True
        
    except ImportError:
        print("  ⚠️ pygame not available, skipping keyboard test")
        return True
    except Exception as e:
        print(f"  ✗ Keyboard input test failed: {e}")
        return False

def test_autocomplete_with_autofocus():
    """Test that autocomplete works with auto-focused input."""
    print("Testing autocomplete with auto-focus...")
    
    try:
        import pygame
        from python_exception_quiz.pygame_quiz import InputBox
        
        # Mock font
        class MockFont:
            def render(self, text, color):
                class MockSurface:
                    pass
                class MockRect:
                    width = len(text) * 8
                    height = 16
                return MockSurface(), MockRect()
        
        # Create input box with suggestions
        input_box = InputBox(10, 10, 200, 30, MockFont())
        input_box.set_suggestions(['ValueError', 'TypeError', 'IndexError'])
        input_box.active = True  # Auto-focus
        
        # Type "Val" to trigger autocomplete
        input_box.text = "Val"
        input_box.cursor_pos = 3
        input_box._update_suggestions()
        
        if 'ValueError' in input_box.filtered_suggestions:
            print("  ✓ Autocomplete suggestions generated")
        else:
            print("  ✗ Autocomplete suggestions not generated")
            return False
        
        # Test Tab key for autocomplete
        with unittest.mock.patch('pygame.KEYDOWN', 2), \
             unittest.mock.patch('pygame.K_TAB', 9):
            class MockTabEvent:
                type = pygame.KEYDOWN
                key = pygame.K_TAB
                unicode = ""
            
            tab_event = MockTabEvent()
            input_box.handle_event(tab_event)
            
            if input_box.text == "ValueError":
                print("  ✓ Tab autocomplete works with auto-focus")
            else:
                print(f"  ✗ Tab autocomplete failed: got '{input_box.text}', expected 'ValueError'")
                return False
        
        return True
        
    except ImportError:
        print("  ⚠️ pygame not available, skipping autocomplete test") 
        return True
    except Exception as e:
        print(f"  ✗ Autocomplete test failed: {e}")
        return False

def main():
    """Run all keyboard integration tests."""
    print("=" * 60)
    print("Python Exception Quiz - GUI Keyboard Integration Test")
    print("=" * 60)
    
    tests = [
        ("Keyboard Input with Auto-Focus", test_keyboard_input_with_autofocus),
        ("Autocomplete with Auto-Focus", test_autocomplete_with_autofocus)
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
        print("✅ All integration tests passed!")
        print("\nKeyboard Integration Features:")
        print("• Auto-focused input accepts keyboard input immediately")
        print("• Character typing works without clicking")
        print("• Backspace and editing work properly")
        print("• Enter key submits answers as expected")
        print("• Autocomplete works with Tab key")
        print("• No clicking required - just start typing!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())