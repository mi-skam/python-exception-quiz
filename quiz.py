#!/usr/bin/env python3
"""
Python Exception Quiz - Main Launcher
Entry point to launch different versions of the game
"""

import argparse
import sys
import os

def _detect_best_interface():
    """Auto-detect the best available interface."""
    # Try GUI first (pygame)
    try:
        import pygame
        return 'gui'
    except ImportError:
        pass
    
    # Try TUI second (curses)
    try:
        import curses
        # Check if we have a terminal
        if os.isatty(sys.stdout.fileno()):
            return 'tui'
    except (ImportError, OSError):
        pass
    
    # Fallback error
    print("ERROR: No compatible interface available!")
    print("Please install pygame for the GUI version:")
    print("  pip install pygame")
    print("Or ensure you have curses support for the TUI version.")
    sys.exit(1)

def _launch_tui(data_dir):
    """Launch TUI version with error handling."""
    try:
        from tui_quiz import main as tui_main
        tui_main(data_dir)
    except ImportError as e:
        print(f"TUI interface error: {e}")
        print("Your system might not support curses.")
        print("Please install pygame for the GUI version:")
        print("  pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"TUI error: {e}")
        print("Try installing pygame for the GUI version:")
        print("  pip install pygame")
        sys.exit(1)

def main():
    """Main launcher for the Python Exception Quiz."""
    parser = argparse.ArgumentParser(
        description="Python Exception Quiz - Test your Python exception knowledge!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Default behavior:
  Automatically launches the best available interface:
  1. GUI (pygame) - if pygame is available
  2. TUI (terminal) - if curses is available
  3. Fallback error message if neither works

Interface options:
  gui     - Force graphical interface (requires pygame)
  tui     - Force terminal interface (requires curses)
  cli     - Simple command-line interface (internal/debug use)

Examples:
  python quiz.py               # Auto-detect best interface
  python quiz.py gui           # Force GUI version
  python quiz.py tui           # Force TUI version
  python quiz.py cli --stats   # Show statistics (debug)
  python quiz.py cli --scores  # Show scores (debug)
        """
    )
    
    parser.add_argument('interface', 
                       choices=['gui', 'tui', 'cli'],
                       nargs='?',
                       help='Force specific interface (optional)')
    
    parser.add_argument('--data-dir', 
                       default='.',
                       help='Directory containing game data files (default: current directory)')
    
    parser.add_argument('--stats', 
                       action='store_true',
                       help='Show current game statistics (CLI only)')
    
    parser.add_argument('--scores', 
                       action='store_true',
                       help='Show high scores (CLI only)')
    
    args = parser.parse_args()
    
    # Validate data directory and required files
    if not os.path.exists(args.data_dir):
        print(f"Error: Data directory '{args.data_dir}' does not exist!")
        sys.exit(1)
    
    levels_file = os.path.join(args.data_dir, 'levels.json')
    if not os.path.exists(levels_file):
        print(f"Error: levels.json not found in '{args.data_dir}'!")
        print("Make sure you're running from the correct directory.")
        sys.exit(1)
    
    # Auto-detect best interface if none specified
    if not args.interface:
        args.interface = _detect_best_interface()
    
    # Launch appropriate interface
    try:
        if args.interface == 'gui':
            if args.stats or args.scores:
                print("--stats and --scores options are only available for CLI interface")
                print("Use: python quiz.py cli --stats")
                sys.exit(1)
                
            try:
                from pygame_quiz import GUIQuizGame
                gui_game = GUIQuizGame(args.data_dir)
                gui_game.run()
            except ImportError:
                print("Pygame is required for the GUI interface.")
                print("Install it with: pip install pygame")
                print("Falling back to TUI version...")
                _launch_tui(args.data_dir)
                
        elif args.interface == 'tui':
            if args.stats or args.scores:
                print("--stats and --scores options are only available for CLI interface")
                print("Use: python quiz.py cli --stats")
                sys.exit(1)
            
            _launch_tui(args.data_dir)
                
        elif args.interface == 'cli':
            from cli_quiz import CLIQuizGame
            cli_game = CLIQuizGame(args.data_dir)
            
            if args.stats:
                cli_game.show_stats()
            elif args.scores:
                cli_game.show_high_scores_only()
            else:
                cli_game.run()
                
    except KeyboardInterrupt:
        print("\\n\\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
