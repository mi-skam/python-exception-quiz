# Python Exception Hierarchy Quiz 🐍

A fun and educational quiz game to test your knowledge of Python's exception hierarchy! Learn which exceptions are raised by different code scenarios through interactive gameplay.

## Quick Start

### Simple Launch (Recommended)
```bash
# Auto-detects and launches the best available interface
python quiz.py
```

The game automatically:
1. **Launch GUI** (if pygame is available)
2. **Fall back to TUI** (if curses is available) 
3. **Shows error** with installation instructions if neither works

## Installation & Setup

### For Best Experience (GUI)
```bash
# Clone and install with GUI support
git clone <repository>
cd python-exception-quiz
pip install -e .[gui]  # Install with pygame
python quiz.py
```

### Development Installation
```bash
# Install in development mode
pip install -e .
python quiz.py
```

### Alternative: Manual Dependencies
```bash
pip install pygame  # For GUI version
python quiz.py
```

## Package Structure

```
python-exception-quiz/
├── src/python_exception_quiz/    # Main package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Launcher with auto-detection
│   ├── game_engine.py           # Core game logic
│   ├── gui_quiz.py              # Pygame GUI version
│   ├── tui_quiz.py              # Terminal UI version
│   ├── cli_quiz.py              # Command-line version (debug)
│   └── levels.json              # Question database
├── test/                        # All test files
│   ├── test_package_structure.py
│   ├── test_esc_functionality.py
│   ├── test_gui_fixes.py
│   └── test_tui_fixes.py
├── main.py                      # Entry point
├── pyproject.toml               # Modern Python packaging
└── README.md                    # This file
```

## Usage Examples

### Normal Gameplay
```bash
# Auto-detect best interface (recommended)
python quiz.py

# Force specific interface
python quiz.py gui    # Pygame GUI
python quiz.py tui    # Terminal UI
```

### Development & Debug
```bash
# View game statistics
python quiz.py cli --stats

# View high scores
python quiz.py cli --scores

# Run tests
python -m pytest test/

# Install in development mode
pip install -e .
```

## Game Features

- **Auto-detected Interface**: Automatically launches the best available interface
- **Multiple Difficulty Levels**: Progress from Simple → Intermediate → Expert  
- **Visual Interfaces**: Beautiful GUI with pygame or rich terminal UI with curses
- **ESC to Quit**: Gracefully exit with score display anytime (Press ESC key or type 'ESC')
- **Progress Saving**: Continue your game later from where you left off
- **High Score Tracking**: Compete with yourself and others
- **Autocomplete Support**: Helpful suggestions for exception names

## Interface Priority

The game auto-detects and launches interfaces in this order:

1. **GUI (pygame)** - Best visual experience with mouse and keyboard controls
2. **TUI (curses)** - Rich terminal interface with colors and visual elements  
3. **Error message** - With clear installation instructions

The CLI version is available for Debug/Development use.

## Game Controls

### GUI Version (pygame)
- **Start Typing**: Input box is auto-focused - no clicking required!
- **Type**: Your answer and press Enter
- **Arrow Keys/Tab**: Navigate autocomplete suggestions  
- **Mouse Wheel**: Scroll code content
- **ESC**: Quit game (with confirmation)

### TUI Version (terminal)
- **Type**: Your answer and press Enter
- **↑↓/Tab**: Navigate autocomplete suggestions
- **ESC**: Quit game (with confirmation)

### CLI Version (debug)
- **Type 'ESC'**: Quit game (with confirmation)
- **Type '?'**: Show all available exceptions
- **Type 'partial?'**: Show suggestions for partial input

## Development

### Package Installation
```bash
# Development installation
pip install -e .

# With GUI dependencies
pip install -e .[gui]

# Test the installation
python -c "import python_exception_quiz; print('Package installed!')"
```

### Running Tests
```bash
# Run all tests
python -m pytest test/

# Run specific test
python -m pytest test/test_package_structure.py

# Run with verbose output
python -m pytest -v test/
```

### Building Distribution
```bash
# Build package
python -m build

# Install from build
pip install dist/python_exception_quiz-1.0.0-py3-none-any.whl
```

## Troubleshooting

### GUI Not Working?
```bash
pip install pygame
python main.py gui
```

### TUI Not Working?
```bash
# Ensure you're in a proper terminal
python main.py tui
```

### Import Errors?
```bash
# Install in development mode
pip install -e .
```

### Force CLI Mode (Debug)
```bash
python main.py cli
```

## Requirements

- **Python 3.6+**
- **pygame** (for GUI, recommended)
- **curses** (for TUI, usually built-in)

## License

MIT License - see LICENSE file for details.

---

**Happy Learning!** 🚀 Test your Python exception knowledge and become a debugging master!