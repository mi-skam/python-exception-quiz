#!/usr/bin/env python3
"""
Python Exception Quiz - TUI Version
Terminal User Interface using curses for a more visual experience
"""

import curses
import sys
import os
import textwrap
from typing import List, Optional
from .game_engine import ExceptionQuizGame

class TUIQuizGame:
    """Terminal User Interface for the Exception Quiz Game."""
    
    def __init__(self, stdscr, data_dir: str = "data"):
        self.stdscr = stdscr
        self.game = ExceptionQuizGame(data_dir)
        self.data_dir = data_dir
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Correct answer
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # Wrong answer
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Warning/highlight
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Info
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Title
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)     # Input field
        
        # Color constants
        self.COLOR_CORRECT = curses.color_pair(1)
        self.COLOR_WRONG = curses.color_pair(2)
        self.COLOR_HIGHLIGHT = curses.color_pair(3)
        self.COLOR_INFO = curses.color_pair(4)
        self.COLOR_TITLE = curses.color_pair(5)
        self.COLOR_INPUT = curses.color_pair(6)
        
        # Screen dimensions
        self.height, self.width = stdscr.getmaxyx()
        
        # Input handling
        self.current_input = ""
        self.autocomplete_suggestions = []
        self.selected_suggestion = 0
    
    def run(self) -> None:
        """Main game loop for TUI version."""
        try:
            curses.curs_set(0)  # Hide cursor initially
        except:
            pass  # Some terminals don't support cursor visibility
        
        try:
            # Welcome screen
            self._show_welcome_screen()
            
            # Check for saved game or start new
            if self.game.has_saved_game():
                if self._ask_yes_no("Continue previous game?"):
                    if self.game.load_game():
                        self._show_message(f"Welcome back, {self.game.player_name}!")
                    else:
                        self._show_message("Failed to load saved game. Starting new game.")
                        self._new_game_setup()
                else:
                    self._new_game_setup()
            else:
                self._new_game_setup()
            
            # Main game loop
            while not self.game.is_game_complete():
                self._play_question()
            
            # Game complete
            self._show_game_complete()
            
        except KeyboardInterrupt:
            self._show_message("Game interrupted. Progress saved!", wait=True)
        finally:
            try:
                curses.curs_set(1)  # Restore cursor
            except:
                pass
    
    def _show_welcome_screen(self) -> None:
        """Show animated welcome screen."""
        self.stdscr.clear()
        
        title_lines = [
            "╔═══════════════════════════════════════════════════════════════╗",
            "║                                                               ║",
            "║        🐍 PYTHON EXCEPTION HIERARCHY QUIZ 🐍                 ║",
            "║                                                               ║",
            "╚═══════════════════════════════════════════════════════════════╝"
        ]
        
        rules = [
            "RULES:",
            "• View Python code that will raise an exception",
            "• Identify which exception type will be raised", 
            "• Type the exact exception name (e.g., 'ValueError')",
            "• Use Tab/Arrow keys for autocomplete suggestions",
            "• Progress: Simple → Intermediate → Expert levels",
            "• Higher levels = more points!",
            "",
            "Controls:",
            "• Tab/↑↓: Navigate autocomplete suggestions",
            "• Enter: Select/Submit answer",
            "• Ctrl+C: Quit (progress will be saved)",
            "",
            "Good luck and have fun learning! 🚀"
        ]
        
        start_y = max(0, (self.height - len(title_lines) - len(rules) - 4) // 2)
        
        # Draw title
        for i, line in enumerate(title_lines):
            x = max(0, (self.width - len(line)) // 2)
            y = start_y + i
            if y < self.height - 1:
                self.stdscr.addstr(y, x, line, self.COLOR_TITLE)
        
        # Draw rules
        start_y += len(title_lines) + 2
        for i, line in enumerate(rules):
            x = max(0, (self.width - len(line)) // 2)
            y = start_y + i
            if y < self.height - 1:
                color = self.COLOR_INFO if not line.startswith("•") else curses.A_NORMAL
                self.stdscr.addstr(y, x, line, color)
        
        # Press any key
        press_key_msg = "Press any key to continue..."
        x = max(0, (self.width - len(press_key_msg)) // 2)
        y = min(self.height - 2, start_y + len(rules) + 2)
        self.stdscr.addstr(y, x, press_key_msg, self.COLOR_HIGHLIGHT)
        
        self.stdscr.refresh()
        self.stdscr.getch()
    
    def _new_game_setup(self) -> None:
        """Set up a new game."""
        self.game.reset_game()
        
        self.stdscr.clear()
        self._draw_header("NEW GAME SETUP")
        
        # Get player name
        self.stdscr.addstr(5, 2, "Enter your name: ", self.COLOR_INFO)
        curses.curs_set(1)
        
        name = ""
        while not name:
            name = self._get_text_input(5, 18, "")
            if not name:
                self.stdscr.addstr(7, 2, "Name cannot be empty! Please try again.", self.COLOR_WRONG)
                self.stdscr.refresh()
        
        self.game.player_name = name
        curses.curs_set(0)
        
        self._show_message(f"Welcome, {name}! Let's test your Python knowledge.", wait=True)
    
    def _play_question(self) -> None:
        """Play a single question with visual interface."""
        question = self.game.get_current_question()
        if not question:
            return
        
        stats = self.game.get_game_stats()
        difficulty, total_questions = self.game.get_level_info(self.game.current_level)
        
        self.stdscr.clear()
        
        # Header with stats
        header = (f"Level {self.game.current_level} ({difficulty.title()}) - "
                 f"Question {stats['current_question']}/{total_questions} | "
                 f"Score: {self.game.score}")
        self._draw_header(header)
        
        # Code section (upper part)
        code_start_y = 3
        self.stdscr.addstr(code_start_y, 2, "CODE:", self.COLOR_TITLE)
        
        # Wrap code lines
        code_lines = question['code'].split('\n')
        wrapped_code = []
        for line in code_lines:
            if len(line) <= self.width - 6:
                wrapped_code.append(line)
            else:
                wrapped_code.extend(textwrap.wrap(line, self.width - 6))
        
        # Draw code box
        code_box_height = min(10, len(wrapped_code) + 2)
        self._draw_box(code_start_y + 1, 2, self.width - 4, code_box_height)
        
        for i, line in enumerate(wrapped_code[:8]):  # Limit lines shown
            if code_start_y + 2 + i < self.height - 10:
                self.stdscr.addstr(code_start_y + 2 + i, 4, line, self.COLOR_INFO)
        
        # Context section (right side)
        context_start_y = code_start_y + code_box_height + 2
        self.stdscr.addstr(context_start_y, 2, f"Context: {question['context']}", self.COLOR_HIGHLIGHT)
        
        # Input section (bottom part)
        input_y = self.height - 8
        self.stdscr.addstr(input_y, 2, "Your answer:", self.COLOR_INFO)
        
        # Get user input with autocomplete
        user_answer = self._get_input_with_autocomplete(input_y + 1, 2)
        
        # Check if user wants to quit
        if user_answer == 'QUIT_GAME':
            self._show_game_complete()
            return
        
        # Check answer and show result
        correct, explanation = self.game.check_answer(user_answer)
        
        result_y = input_y + 4
        if correct:
            points = 10 * self.game.current_level
            result_text = f"✅ CORRECT! +{points} points"
            self.stdscr.addstr(result_y, 2, result_text, self.COLOR_CORRECT)
        else:
            result_text = f"❌ INCORRECT! Answer: {question['correct_answer']}"
            self.stdscr.addstr(result_y, 2, result_text, self.COLOR_WRONG)
        
        # Show explanation
        if result_y + 1 < self.height - 1:
            explanation_wrapped = textwrap.wrap(f"Explanation: {explanation}", 
                                              self.width - 4)
            for i, line in enumerate(explanation_wrapped):
                if result_y + 2 + i < self.height - 1:
                    self.stdscr.addstr(result_y + 2 + i, 2, line)
        
        # Save progress
        self.game.save_game()
        
        self.stdscr.addstr(self.height - 1, 2, "Press any key to continue...", 
                          self.COLOR_HIGHLIGHT)
        self.stdscr.refresh()
        self.stdscr.getch()
        
        # Move to next question
        if not self.game.next_question():
            return
        
        # Level complete notification
        if self.game.current_question == 0 and not self.game.is_game_complete():
            self._show_message("🎉 Level Complete! Moving to next level...", wait=True)
    
    def _get_input_with_autocomplete(self, y: int, x: int) -> str:
        """Get input with visual autocomplete support."""
        curses.curs_set(1)
        self.current_input = ""
        self.autocomplete_suggestions = []
        self.selected_suggestion = 0
        
        # Input box
        input_width = min(40, self.width - x - 2)
        self._draw_box(y, x, input_width, 1)
        
        while True:
            # Clear input area
            self.stdscr.addstr(y + 1, x + 1, " " * (input_width - 2))
            
            # Show current input
            display_input = self.current_input[-input_width + 3:] if len(self.current_input) > input_width - 3 else self.current_input
            self.stdscr.addstr(y + 1, x + 1, display_input, self.COLOR_INPUT)
            
            # Update autocomplete suggestions
            if self.current_input:
                self.autocomplete_suggestions = self.game.get_autocomplete_suggestions(self.current_input)
            else:
                self.autocomplete_suggestions = self.game.get_autocomplete_suggestions("")[:8]
            
            # Show suggestions
            self._show_autocomplete_suggestions(y + 3, x)
            
            # Position cursor
            cursor_x = min(x + 1 + len(display_input), x + input_width - 2)
            self.stdscr.move(y + 1, cursor_x)
            self.stdscr.refresh()
            
            # Handle input
            key = self.stdscr.getch()
            
            if key == ord('\n'):  # Enter
                if self.autocomplete_suggestions and 0 <= self.selected_suggestion < len(self.autocomplete_suggestions):
                    result = self.autocomplete_suggestions[self.selected_suggestion]
                else:
                    result = self.current_input
                break
            elif key == ord('\t'):  # Tab - select current suggestion
                if self.autocomplete_suggestions and 0 <= self.selected_suggestion < len(self.autocomplete_suggestions):
                    self.current_input = self.autocomplete_suggestions[self.selected_suggestion]
                    self.selected_suggestion = 0
            elif key == curses.KEY_UP:
                if self.autocomplete_suggestions:
                    self.selected_suggestion = (self.selected_suggestion - 1) % len(self.autocomplete_suggestions)
            elif key == curses.KEY_DOWN:
                if self.autocomplete_suggestions:
                    self.selected_suggestion = (self.selected_suggestion + 1) % len(self.autocomplete_suggestions)
            elif key == curses.KEY_BACKSPACE or key == 127:
                if self.current_input:
                    self.current_input = self.current_input[:-1]
                    self.selected_suggestion = 0
            elif key == 27:  # Escape
                if self._ask_quit_game():
                    result = 'QUIT_GAME'
                    break
                continue
            elif 32 <= key <= 126:  # Printable characters
                self.current_input += chr(key)
                self.selected_suggestion = 0
        
        curses.curs_set(0)
        return result if 'result' in locals() else self.current_input
    
    def _show_autocomplete_suggestions(self, y: int, x: int) -> None:
        """Show autocomplete suggestions in a nice box."""
        if not self.autocomplete_suggestions:
            return
        
        max_suggestions = min(8, len(self.autocomplete_suggestions))
        box_width = min(30, max(len(sugg) for sugg in self.autocomplete_suggestions[:max_suggestions]) + 4)
        
        if y + max_suggestions + 2 > self.height or x + box_width > self.width:
            return
        
        self._draw_box(y, x, box_width, max_suggestions)
        
        for i, suggestion in enumerate(self.autocomplete_suggestions[:max_suggestions]):
            color = self.COLOR_HIGHLIGHT if i == self.selected_suggestion else curses.A_NORMAL
            self.stdscr.addstr(y + 1 + i, x + 1, suggestion, color)
    
    def _draw_header(self, title: str) -> None:
        """Draw header with title."""
        # Clear first line
        self.stdscr.addstr(0, 0, " " * (self.width - 1))
        
        # Center title
        x = max(0, (self.width - len(title)) // 2)
        self.stdscr.addstr(0, x, title, self.COLOR_TITLE)
        
        # Draw line underneath
        self.stdscr.addstr(1, 0, "─" * (self.width - 1))
    
    def _draw_box(self, y: int, x: int, width: int, height: int) -> None:
        """Draw a simple box."""
        if y >= self.height or x >= self.width:
            return
        
        # Corners and borders
        try:
            self.stdscr.addstr(y, x, "┌" + "─" * (width - 2) + "┐")
            for i in range(height):
                self.stdscr.addstr(y + 1 + i, x, "│")
                self.stdscr.addstr(y + 1 + i, x + width - 1, "│")
            self.stdscr.addstr(y + height + 1, x, "└" + "─" * (width - 2) + "┘")
        except curses.error:
            pass  # Ignore if drawing outside screen
    
    def _get_text_input(self, y: int, x: int, prompt: str = "") -> str:
        """Get simple text input."""
        curses.curs_set(1)
        result = ""
        
        while True:
            # Clear line
            self.stdscr.addstr(y, x, " " * (self.width - x - 1))
            
            # Show prompt and current input
            display_text = prompt + result
            self.stdscr.addstr(y, x, display_text[:self.width - x - 1])
            
            # Position cursor
            cursor_pos = min(x + len(display_text), self.width - 1)
            self.stdscr.move(y, cursor_pos)
            self.stdscr.refresh()
            
            key = self.stdscr.getch()
            
            if key == ord('\n'):
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                if result:
                    result = result[:-1]
            elif 32 <= key <= 126:  # Printable characters
                if len(prompt + result) < self.width - x - 2:
                    result += chr(key)
        
        curses.curs_set(0)
        return result.strip()
    
    def _ask_yes_no(self, question: str) -> bool:
        """Ask yes/no question with visual interface."""
        self.stdscr.clear()
        self._draw_header("QUESTION")
        
        # Show question
        question_y = self.height // 2 - 2
        x = max(0, (self.width - len(question)) // 2)
        self.stdscr.addstr(question_y, x, question, self.COLOR_INFO)
        
        # Show options
        options = "Press 'y' for Yes, 'n' for No"
        x = max(0, (self.width - len(options)) // 2)
        self.stdscr.addstr(question_y + 2, x, options, self.COLOR_HIGHLIGHT)
        
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()
            if key in [ord('y'), ord('Y')]:
                return True
            elif key in [ord('n'), ord('N')]:
                return False
    
    def _ask_quit_game(self) -> bool:
        """Ask if the player wants to quit the game."""
        self.stdscr.clear()
        self._draw_header("QUIT GAME?")
        
        # Show quit message
        quit_lines = [
            "Do you want to quit the current game?",
            "",
            "Your progress will be saved.",
            "You can continue later from where you left off."
        ]
        
        start_y = self.height // 2 - 3
        for i, line in enumerate(quit_lines):
            x = max(0, (self.width - len(line)) // 2)
            y = start_y + i
            if y < self.height - 3:
                color = self.COLOR_INFO if line else curses.A_NORMAL
                self.stdscr.addstr(y, x, line, color)
        
        # Show options
        options = "Press 'y' to Quit, 'n' to Continue Playing"
        x = max(0, (self.width - len(options)) // 2)
        self.stdscr.addstr(start_y + len(quit_lines) + 1, x, options, self.COLOR_HIGHLIGHT)
        
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()
            if key in [ord('y'), ord('Y')]:
                return True
            elif key in [ord('n'), ord('N')]:
                return False
    
    def _show_message(self, message: str, wait: bool = False) -> None:
        """Show a centered message."""
        self.stdscr.clear()
        
        # Center message
        lines = textwrap.wrap(message, self.width - 4)
        start_y = max(0, (self.height - len(lines)) // 2)
        
        for i, line in enumerate(lines):
            x = max(0, (self.width - len(line)) // 2)
            y = start_y + i
            if y < self.height:
                self.stdscr.addstr(y, x, line, self.COLOR_INFO)
        
        if wait:
            wait_msg = "Press any key to continue..."
            x = max(0, (self.width - len(wait_msg)) // 2)
            y = min(self.height - 2, start_y + len(lines) + 2)
            self.stdscr.addstr(y, x, wait_msg, self.COLOR_HIGHLIGHT)
            self.stdscr.refresh()
            self.stdscr.getch()
        else:
            self.stdscr.refresh()
    
    def _show_game_complete(self) -> None:
        """Show game completion screen with stats and high scores."""
        self.stdscr.clear()
        
        # Title
        title = "🎊 CONGRATULATIONS! 🎊"
        x = max(0, (self.width - len(title)) // 2)
        self.stdscr.addstr(2, x, title, self.COLOR_TITLE)
        
        # Stats
        stats = self.game.get_game_stats()
        stats_lines = [
            "You've completed the Python Exception Quiz!",
            "",
            f"Final Score: {self.game.score}",
            f"Questions: {stats['completed_questions']}/{stats['total_questions']}",
            f"Accuracy: {stats['progress']:.1f}%"
        ]
        
        start_y = 5
        for i, line in enumerate(stats_lines):
            x = max(0, (self.width - len(line)) // 2)
            self.stdscr.addstr(start_y + i, x, line, self.COLOR_INFO)
        
        # Save high score
        self.game.save_high_score()
        
        # Show high scores
        high_scores = self.game.get_high_scores()
        if high_scores:
            scores_start_y = start_y + len(stats_lines) + 2
            self.stdscr.addstr(scores_start_y, 2, "🏆 HIGH SCORES 🏆", self.COLOR_TITLE)
            
            headers = f"{'Rank':<6}{'Name':<15}{'Score':<10}{'Level':<8}"
            self.stdscr.addstr(scores_start_y + 1, 2, headers, self.COLOR_HIGHLIGHT)
            self.stdscr.addstr(scores_start_y + 2, 2, "─" * len(headers))
            
            for i, score in enumerate(high_scores[:8], 1):  # Show top 8
                if scores_start_y + 3 + i < self.height - 2:
                    score_line = f"{i:<6}{score['name']:<15}{score['score']:<10}{score['level_reached']:<8}"
                    color = self.COLOR_HIGHLIGHT if score['name'] == self.game.player_name else curses.A_NORMAL
                    self.stdscr.addstr(scores_start_y + 3 + i, 2, score_line, color)
        
        # Exit instruction
        self.stdscr.addstr(self.height - 1, 2, "Press any key to exit...", self.COLOR_HIGHLIGHT)
        self.stdscr.refresh()
        self.stdscr.getch()
        
        # Clean up save file
        try:
            os.remove(os.path.join(self.data_dir, "savegame.json"))
        except FileNotFoundError:
            pass

def main(data_dir: str = "data"):
    """Main entry point for TUI version."""
    def tui_main(stdscr):
        # Fix terminal initialization
        try:
            # Initialize curses properly
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(True)
            stdscr.clear()
            stdscr.refresh()
            
            tui_game = TUIQuizGame(stdscr, data_dir)
            tui_game.run()
        finally:
            # Clean up terminal settings
            try:
                curses.nocbreak()
                stdscr.keypad(False)
                curses.echo()
                curses.endwin()
            except:
                pass
    
    try:
        # Check if terminal supports curses
        if not os.isatty(sys.stdout.fileno()):
            print("Error: This program requires an interactive terminal.")
            print("Try running the CLI version instead: python cli_quiz.py")
            return
            
        # Initialize and run
        stdscr = curses.initscr()
        try:
            tui_main(stdscr)
        finally:
            curses.endwin()
    except Exception as e:
        # Make sure terminal is restored
        try:
            curses.endwin()
        except:
            pass
        print(f"TUI Error: {e}")
        print("Your terminal might not support all features.")
        print("Try running the CLI version instead: python cli_quiz.py")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python Exception Quiz - TUI Version")
    parser.add_argument('--data-dir', default='.',
                       help='Directory containing game data files')
    args = parser.parse_args()
    main(args.data_dir)
