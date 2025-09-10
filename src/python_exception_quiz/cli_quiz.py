#!/usr/bin/env python3
"""
Python Exception Quiz - CLI Version
Simple command-line interface for the quiz game
"""

import argparse
import sys
import os
from typing import List, Optional
from .game_engine import ExceptionQuizGame

class CLIQuizGame:
    """Command-line interface for the Exception Quiz Game."""
    
    def __init__(self, data_dir: str = "data"):
        self.game = ExceptionQuizGame(data_dir)
        self.data_dir = data_dir
    
    def run(self) -> None:
        """Main game loop for CLI version."""
        self._show_welcome()
        
        # Check for saved game
        if self.game.has_saved_game():
            if self._ask_yes_no("Continue previous game?"):
                if self.game.load_game():
                    print(f"Welcome back, {self.game.player_name}!")
                    print(f"Score: {self.game.score}, Level: {self.game.current_level}")
                else:
                    print("Failed to load saved game. Starting new game.")
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
    
    def _show_welcome(self) -> None:
        """Show welcome screen and rules."""
        print("=" * 60)
        print("🐍 PYTHON EXCEPTION HIERARCHY QUIZ 🐍")
        print("=" * 60)
        print()
        print("Welcome to the Python Exception Quiz!")
        print()
        print("RULES:")
        print("• You'll see Python code that will raise an exception")
        print("• Your job is to identify which exception type will be raised")
        print("• Type the exact exception name (e.g., 'ValueError', 'IndexError')")
        print("• Use Tab for autocomplete suggestions")
        print("• Progress through Simple → Intermediate → Expert levels")
        print("• Higher levels give more points!")
        print()
        print("Good luck and have fun learning! 🚀")
        print()
    
    def _new_game_setup(self) -> None:
        """Set up a new game."""
        self.game.reset_game()
        
        print("Starting new game!")
        name = input("Enter your name: ").strip()
        while not name:
            name = input("Please enter your name: ").strip()
        
        self.game.player_name = name
        print(f"Welcome, {name}! Let's test your Python exception knowledge.")
        print()
    
    def _play_question(self) -> None:
        """Play a single question."""
        question = self.game.get_current_question()
        if not question:
            return
        
        stats = self.game.get_game_stats()
        difficulty, total_questions = self.game.get_level_info(self.game.current_level)
        
        print("-" * 60)
        print(f"Level {self.game.current_level} ({difficulty.title()}) - "
              f"Question {stats['current_question']}/{total_questions}")
        print(f"Score: {self.game.score}")
        print("-" * 60)
        print()
        print("CODE:")
        print("```python")
        print(question['code'])
        print("```")
        print()
        print(f"Context: {question['context']}")
        print()
        
        # Get user answer with autocomplete hints
        user_answer = self._get_user_input_with_autocomplete()
        
        # Check if user wants to quit
        if user_answer == 'QUIT_GAME':
            self._show_game_complete()
            return
        
        # Check answer
        correct, explanation = self.game.check_answer(user_answer)
        
        print()
        if correct:
            print("✅ Correct!")
            print(f"Earned {10 * self.game.current_level} points!")
        else:
            print("❌ Incorrect!")
            print(f"The correct answer is: {question['correct_answer']}")
        
        print(f"Explanation: {explanation}")
        print()
        
        # Save progress
        self.game.save_game()
        
        # Move to next question
        if not self.game.next_question():
            return
        
        # Level complete notification
        if self.game.current_question == 0 and not self.game.is_game_complete():
            print("🎉 Level Complete! Moving to next level...")
            input("Press Enter to continue...")
            print()
    
    def _get_user_input_with_autocomplete(self) -> str:
        """Get user input with autocomplete suggestions."""
        while True:
            try:
                user_input = input("Your answer (type '?' for suggestions, 'ESC' to quit): ").strip()
                
                if user_input.upper() == 'ESC':
                    if self._ask_quit_game():
                        return 'QUIT_GAME'
                    continue
                elif user_input == '?':
                    suggestions = self.game.get_autocomplete_suggestions("")
                    print("\\nAvailable exceptions:")
                    self._show_suggestions(suggestions[:20])  # Show more in CLI
                    continue
                elif user_input.endswith('?'):
                    # Show suggestions for partial input
                    prefix = user_input[:-1]
                    suggestions = self.game.get_autocomplete_suggestions(prefix)
                    if suggestions:
                        print(f"\\nSuggestions for '{prefix}':")
                        self._show_suggestions(suggestions)
                    else:
                        print(f"\\nNo suggestions found for '{prefix}'")
                    continue
                elif user_input:
                    return user_input
                else:
                    print("Please enter an answer (or '?' for help, 'ESC' to quit)")
                    
            except KeyboardInterrupt:
                if self._ask_quit_game():
                    return 'QUIT_GAME'
                continue
            except EOFError:
                print("\\n\\nGame ended. Progress saved!")
                sys.exit(0)
    
    def _show_suggestions(self, suggestions: List[str]) -> None:
        """Show autocomplete suggestions in a nice format."""
        if not suggestions:
            return
        
        # Show in columns
        cols = 3
        for i in range(0, len(suggestions), cols):
            row = suggestions[i:i+cols]
            print("  " + "".join(f"{exc:<25}" for exc in row))
        print()
    
    def _show_game_complete(self) -> None:
        """Show game completion screen."""
        stats = self.game.get_game_stats()
        
        print("🎊 CONGRATULATIONS! 🎊")
        print("You've completed the Python Exception Quiz!")
        print()
        print(f"Final Score: {self.game.score}")
        print(f"Questions Completed: {stats['completed_questions']}/{stats['total_questions']}")
        print(f"Accuracy: {stats['progress']:.1f}%")
        print()
        
        # Save high score
        self.game.save_high_score()
        
        # Show high scores
        self._show_high_scores()
        
        # Clean up
        try:
            os.remove(os.path.join(self.data_dir, "savegame.json"))
        except FileNotFoundError:
            pass
    
    def _show_high_scores(self) -> None:
        """Display high scores."""
        high_scores = self.game.get_high_scores()
        if not high_scores:
            print("No high scores yet!")
            return
        
        print("🏆 HIGH SCORES 🏆")
        print("-" * 40)
        print(f"{'Rank':<6}{'Name':<15}{'Score':<10}{'Level':<8}")
        print("-" * 40)
        
        for i, score in enumerate(high_scores[:10], 1):
            print(f"{i:<6}{score['name']:<15}{score['score']:<10}{score['level_reached']:<8}")
        print()
    
    def _ask_yes_no(self, question: str) -> bool:
        """Ask a yes/no question."""
        while True:
            answer = input(f"{question} (y/n): ").strip().lower()
            if answer in ('y', 'yes'):
                return True
            elif answer in ('n', 'no'):
                return False
            else:
                print("Please answer 'y' or 'n'")
    
    def _ask_quit_game(self) -> bool:
        """Ask if the player wants to quit the game."""
        print("\\n" + "=" * 40)
        print("Do you want to quit the current game?")
        print("Your progress will be saved.")
        print("=" * 40)
        return self._ask_yes_no("Quit game?")
    
    def show_stats(self) -> None:
        """Show current game statistics."""
        if not self.game.has_saved_game():
            print("No saved game found.")
            return
        
        if self.game.load_game():
            stats = self.game.get_game_stats()
            print("Current Game Statistics:")
            print(f"Player: {stats['player_name']}")
            print(f"Level: {stats['current_level']}")
            print(f"Question: {stats['current_question']}")
            print(f"Score: {stats['score']}")
            print(f"Progress: {stats['progress']:.1f}%")
        else:
            print("Failed to load saved game.")
    
    def show_high_scores_only(self) -> None:
        """Show only the high scores."""
        self._show_high_scores()

def main():
    """Main entry point for CLI version."""
    parser = argparse.ArgumentParser(description="Python Exception Quiz - CLI Version")
    parser.add_argument('--stats', action='store_true', 
                       help='Show current game statistics')
    parser.add_argument('--scores', action='store_true',
                       help='Show high scores')
    parser.add_argument('--data-dir', default='.',
                       help='Directory containing game data files')
    
    args = parser.parse_args()
    
    # Set up game with correct data directory
    cli_game = CLIQuizGame(args.data_dir)
    
    if args.stats:
        cli_game.show_stats()
    elif args.scores:
        cli_game.show_high_scores_only()
    else:
        cli_game.run()

if __name__ == "__main__":
    main()
