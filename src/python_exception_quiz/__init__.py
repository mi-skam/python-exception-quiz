"""
Python Exception Quiz - A fun and educational quiz game to test your knowledge of Python's exception hierarchy!

This package provides multiple interfaces:
- GUI (pygame): Rich graphical interface
- TUI (curses): Terminal-based interface
- CLI: Simple command-line interface (for debugging)

The main launcher automatically detects and uses the best available interface.
"""

__version__ = "1.0.0"
__author__ = "Python Exception Quiz Team"

# Import main components for easy access
from .game_engine import ExceptionQuizGame

__all__ = ["ExceptionQuizGame"]