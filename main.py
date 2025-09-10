#!/usr/bin/env python3
"""
Python Exception Quiz - Entry Point
Launches the quiz with auto-detection of the best available interface
"""

def main():
    """Main entry point that launches the quiz."""
    try:
        from src.python_exception_quiz.main import main as quiz_main
        quiz_main()
    except ImportError:
        # Fallback for when package is properly installed
        from python_exception_quiz.main import main as quiz_main
        quiz_main()

if __name__ == "__main__":
    main()