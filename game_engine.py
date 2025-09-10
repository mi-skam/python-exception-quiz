#!/usr/bin/env python3
"""
Python Exception Quiz Game - Core Engine
A fun quiz game to test your knowledge of Python's exception hierarchy!
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class ExceptionQuizGame:
    """Core game engine for the Python Exception Quiz."""
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.levels_file = os.path.join(data_dir, "levels.json")
        self.scores_file = os.path.join(data_dir, "highscores.json")
        self.save_file = os.path.join(data_dir, "savegame.json")
        
        # Python exception hierarchy for autocomplete
        self.python_exceptions = [
            'BaseException', 'SystemExit', 'KeyboardInterrupt', 'GeneratorExit',
            'Exception', 'StopIteration', 'StopAsyncIteration', 'ArithmeticError',
            'FloatingPointError', 'OverflowError', 'ZeroDivisionError',
            'AssertionError', 'AttributeError', 'BufferError', 'EOFError',
            'ImportError', 'ModuleNotFoundError', 'LookupError', 'IndexError',
            'KeyError', 'MemoryError', 'NameError', 'UnboundLocalError',
            'OSError', 'BlockingIOError', 'ChildProcessError', 'ConnectionError',
            'BrokenPipeError', 'ConnectionAbortedError', 'ConnectionRefusedError',
            'ConnectionResetError', 'FileExistsError', 'FileNotFoundError',
            'InterruptedError', 'IsADirectoryError', 'NotADirectoryError',
            'PermissionError', 'ProcessLookupError', 'TimeoutError',
            'ReferenceError', 'RuntimeError', 'NotImplementedError',
            'RecursionError', 'SyntaxError', 'IndentationError', 'TabError',
            'SystemError', 'TypeError', 'ValueError', 'UnicodeError',
            'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeTranslateError',
            'Warning', 'DeprecationWarning', 'PendingDeprecationWarning',
            'RuntimeWarning', 'SyntaxWarning', 'UserWarning', 'FutureWarning',
            'ImportWarning', 'UnicodeWarning', 'BytesWarning', 'ResourceWarning'
        ]
        
        self.levels = self._load_levels()
        self.current_level = 1
        self.current_question = 0
        self.score = 0
        self.player_name = ""
        
    def _load_levels(self) -> Dict:
        """Load quiz levels from JSON file."""
        try:
            with open(self.levels_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.levels_file} not found!")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.levels_file}")
            sys.exit(1)
    
    def get_current_question(self) -> Optional[Dict]:
        """Get the current question data."""
        level_data = self._get_level_data(self.current_level)
        if not level_data or self.current_question >= len(level_data['questions']):
            return None
        return level_data['questions'][self.current_question]
    
    def _get_level_data(self, level: int) -> Optional[Dict]:
        """Get data for a specific level."""
        for level_data in self.levels['levels']:
            if level_data['level'] == level:
                return level_data
        return None
    
    def get_level_info(self, level: int) -> Tuple[str, int]:
        """Get level difficulty and question count."""
        level_data = self._get_level_data(level)
        if level_data:
            return level_data['difficulty'], len(level_data['questions'])
        return "unknown", 0
    
    def check_answer(self, user_answer: str) -> Tuple[bool, str]:
        """Check if the user's answer is correct."""
        question = self.get_current_question()
        if not question:
            return False, "No current question"
        
        correct = user_answer.strip() == question['correct_answer']
        if correct:
            self.score += 10 * self.current_level  # More points for harder levels
        
        return correct, question['explanation']
    
    def next_question(self) -> bool:
        """Move to the next question. Returns True if successful, False if level/game complete."""
        level_data = self._get_level_data(self.current_level)
        if not level_data:
            return False
            
        self.current_question += 1
        
        # Check if level is complete
        if self.current_question >= len(level_data['questions']):
            return self._next_level()
        
        return True
    
    def _next_level(self) -> bool:
        """Move to the next level."""
        self.current_level += 1
        self.current_question = 0
        
        # Check if game is complete
        if self._get_level_data(self.current_level) is None:
            return False  # Game complete
        
        return True
    
    def is_game_complete(self) -> bool:
        """Check if the game is complete."""
        return self._get_level_data(self.current_level) is None
    
    def get_autocomplete_suggestions(self, prefix: str) -> List[str]:
        """Get autocomplete suggestions for exception names."""
        prefix = prefix.strip()
        if not prefix:
            return self.python_exceptions[:10]  # Return first 10 if no prefix
        
        suggestions = [exc for exc in self.python_exceptions 
                      if exc.lower().startswith(prefix.lower())]
        return suggestions[:10]  # Limit to 10 suggestions
    
    def save_game(self) -> None:
        """Save the current game state."""
        save_data = {
            'player_name': self.player_name,
            'current_level': self.current_level,
            'current_question': self.current_question,
            'score': self.score,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save game: {e}")
    
    def load_game(self) -> bool:
        """Load a saved game state. Returns True if successful."""
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            self.player_name = save_data['player_name']
            self.current_level = save_data['current_level']
            self.current_question = save_data['current_question']
            self.score = save_data['score']
            
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False
    
    def has_saved_game(self) -> bool:
        """Check if a saved game exists."""
        return os.path.exists(self.save_file)
    
    def save_high_score(self) -> None:
        """Save the current score to high scores."""
        if not self.player_name:
            return
        
        # Load existing scores
        high_scores = self._load_high_scores()
        
        # Add new score
        new_score = {
            'name': self.player_name,
            'score': self.score,
            'level_reached': self.current_level,
            'timestamp': datetime.now().isoformat()
        }
        
        high_scores.append(new_score)
        
        # Sort by score (descending) and keep top 10
        high_scores.sort(key=lambda x: x['score'], reverse=True)
        high_scores = high_scores[:10]
        
        # Save back to file
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(high_scores, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save high score: {e}")
    
    def _load_high_scores(self) -> List[Dict]:
        """Load high scores from file."""
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_high_scores(self) -> List[Dict]:
        """Get the current high scores."""
        return self._load_high_scores()
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.current_level = 1
        self.current_question = 0
        self.score = 0
        # Don't reset player_name - they might want to play again
        
        # Remove saved game
        try:
            os.remove(self.save_file)
        except FileNotFoundError:
            pass
    
    def get_game_stats(self) -> Dict:
        """Get current game statistics."""
        total_questions = sum(len(level['questions']) for level in self.levels['levels'])
        completed_questions = sum(len(self._get_level_data(i)['questions']) 
                                 for i in range(1, self.current_level)) + self.current_question
        
        return {
            'player_name': self.player_name,
            'current_level': self.current_level,
            'current_question': self.current_question + 1,  # 1-indexed for display
            'score': self.score,
            'total_questions': total_questions,
            'completed_questions': completed_questions,
            'progress': (completed_questions / total_questions) * 100 if total_questions > 0 else 0
        }

if __name__ == "__main__":
    # Simple test
    game = ExceptionQuizGame()
    print("Python Exception Quiz Game Engine")
    print("Available exception types:", len(game.python_exceptions))
    print("Loaded levels:", len(game.levels['levels']))
    
    # Test autocomplete
    print("\\nAutocomplete test for 'Value':")
    suggestions = game.get_autocomplete_suggestions("Value")
    print(suggestions)
