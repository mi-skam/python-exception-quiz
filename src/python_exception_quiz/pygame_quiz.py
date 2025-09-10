#!/usr/bin/env python3
"""
Python Exception Quiz - Pygame GUI Version
Graphical user interface using pygame for the best visual experience
"""

import pygame
import pygame.freetype
import sys
import os
import textwrap
from typing import List, Optional, Tuple
from .game_engine import ExceptionQuizGame

# Colors
COLORS = {
    'background': (30, 30, 40),
    'surface': (45, 45, 60),
    'primary': (100, 150, 255),
    'secondary': (200, 150, 100),
    'success': (100, 255, 150),
    'error': (255, 100, 100),
    'warning': (255, 200, 100),
    'text': (240, 240, 250),
    'text_dim': (180, 180, 190),
    'border': (100, 100, 120),
    'input_bg': (60, 60, 80),
    'input_active': (80, 80, 100)
}

class Button:
    """Simple button class for pygame."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 font, color: Tuple[int, int, int] = COLORS['primary']):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hovered = False
        self.clicked = False
    
    def handle_event(self, event) -> bool:
        """Handle mouse events. Returns True if clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
        
        return False
    
    def draw(self, screen):
        """Draw the button."""
        color = self.color
        if self.hovered and not self.clicked:
            color = tuple(min(255, c + 30) for c in color)
        elif self.clicked:
            color = tuple(max(0, c - 30) for c in color)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLORS['border'], self.rect, 2)
        
        # Center text
        text_surface, text_rect = self.font.render(self.text, COLORS['text'])
        text_x = self.rect.x + (self.rect.width - text_rect.width) // 2
        text_y = self.rect.y + (self.rect.height - text_rect.height) // 2
        screen.blit(text_surface, (text_x, text_y))

class InputBox:
    """Text input box with autocomplete support."""
    
    def __init__(self, x: int, y: int, width: int, height: int, font, 
                 suggestions: List[str] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.active = False
        self.suggestions = suggestions or []
        self.filtered_suggestions = []
        self.selected_suggestion = 0
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def handle_event(self, event) -> bool:
        """Handle input events. Returns True if Enter was pressed."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clicking on the input box activates it
            if self.rect.collidepoint(event.pos):
                self.active = True
            # Don't deactivate on outside clicks during gameplay - keep focus
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # Use selected suggestion if available
                if (self.filtered_suggestions and 
                    0 <= self.selected_suggestion < len(self.filtered_suggestions)):
                    self.text = self.filtered_suggestions[self.selected_suggestion]
                return True
            
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    self._update_suggestions()
            
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                    self._update_suggestions()
            
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            
            elif event.key == pygame.K_UP:
                if self.filtered_suggestions:
                    self.selected_suggestion = (self.selected_suggestion - 1) % len(self.filtered_suggestions)
            
            elif event.key == pygame.K_DOWN:
                if self.filtered_suggestions:
                    self.selected_suggestion = (self.selected_suggestion + 1) % len(self.filtered_suggestions)
            
            elif event.key == pygame.K_TAB:
                # Auto-complete with selected suggestion
                if (self.filtered_suggestions and 
                    0 <= self.selected_suggestion < len(self.filtered_suggestions)):
                    self.text = self.filtered_suggestions[self.selected_suggestion]
                    self.cursor_pos = len(self.text)
                    self._update_suggestions()
            
            elif event.unicode and event.unicode.isprintable():
                self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                self.cursor_pos += 1
                self._update_suggestions()
        
        return False
    
    def _update_suggestions(self):
        """Update filtered suggestions based on current text."""
        if not self.text:
            self.filtered_suggestions = self.suggestions[:10]
        else:
            self.filtered_suggestions = [
                s for s in self.suggestions 
                if s.lower().startswith(self.text.lower())
            ][:10]
        self.selected_suggestion = 0
    
    def update(self, dt: float):
        """Update cursor blink."""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        """Draw the input box."""
        # Background
        bg_color = COLORS['input_active'] if self.active else COLORS['input_bg']
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, COLORS['border'], self.rect, 2)
        
        # Text
        if self.text:
            text_surface, text_rect = self.font.render(self.text, COLORS['text'])
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        
        # Cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5
            if self.text:
                cursor_text = self.text[:self.cursor_pos]
                cursor_surface, cursor_rect = self.font.render(cursor_text, COLORS['text'])
                cursor_x += cursor_rect.width
            
            pygame.draw.line(screen, COLORS['text'], 
                           (cursor_x, self.rect.y + 5), 
                           (cursor_x, self.rect.bottom - 5), 2)
        
        # Suggestions dropdown
        if self.active and self.filtered_suggestions:
            self._draw_suggestions(screen)
    
    def _draw_suggestions(self, screen):
        """Draw autocomplete suggestions."""
        suggestion_height = 25
        dropdown_height = min(len(self.filtered_suggestions) * suggestion_height, 200)
        dropdown_rect = pygame.Rect(
            self.rect.x, 
            self.rect.bottom + 2,
            self.rect.width,
            dropdown_height
        )
        
        pygame.draw.rect(screen, COLORS['surface'], dropdown_rect)
        pygame.draw.rect(screen, COLORS['border'], dropdown_rect, 2)
        
        for i, suggestion in enumerate(self.filtered_suggestions[:8]):
            y = dropdown_rect.y + i * suggestion_height
            suggestion_rect = pygame.Rect(dropdown_rect.x, y, dropdown_rect.width, suggestion_height)
            
            if i == self.selected_suggestion:
                pygame.draw.rect(screen, COLORS['primary'], suggestion_rect)
            
            text_surface, text_rect = self.font.render(suggestion, COLORS['text'])
            screen.blit(text_surface, (suggestion_rect.x + 5, suggestion_rect.y + 2))
    
    def set_suggestions(self, suggestions: List[str]):
        """Update the suggestions list."""
        self.suggestions = suggestions
        self._update_suggestions()

class GUIQuizGame:
    """Pygame GUI for the Exception Quiz Game."""
    
    def __init__(self, data_dir: str = "data"):
        pygame.init()
        pygame.freetype.init()
        
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Python Exception Hierarchy Quiz")
        
        # Load fonts - Use SysFont which works in PyInstaller bundles
        # pygame.freetype.Font(None) doesn't work in bundles, but SysFont does
        self.font_code = pygame.freetype.SysFont('Courier New', 20)
        self.font_large = pygame.freetype.SysFont('Arial', 32)
        self.font_medium = pygame.freetype.SysFont('Arial', 24) 
        self.font_small = pygame.freetype.SysFont('Arial', 18)
        
        self.clock = pygame.time.Clock()
        self.game = ExceptionQuizGame(data_dir)
        self.data_dir = data_dir
        
        # Game state
        self.state = "welcome"  # welcome, menu, playing, complete
        self.input_box = None
        self.buttons = []
        
        # UI elements
        self.scroll_offset = 0
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self._handle_event(event)
            
            # Update
            self._update(dt)
            
            # Draw
            self._draw()
            
            pygame.display.flip()
        
        pygame.quit()
    
    def _handle_event(self, event):
        """Handle events based on current state."""
        if self.state == "welcome":
            self._handle_welcome_event(event)
        elif self.state == "menu":
            self._handle_menu_event(event)
        elif self.state == "playing":
            self._handle_playing_event(event)
        elif self.state == "complete":
            self._handle_complete_event(event)
    
    def _handle_welcome_event(self, event):
        """Handle welcome screen events."""
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.state = "menu"
    
    def _handle_menu_event(self, event):
        """Handle main menu events."""
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            key = event.unicode.lower() if event.unicode else None
            
            if key == 'n':
                self._start_new_game()
                return
            elif key == 'c' and self.game.has_saved_game():
                if self.game.load_game():
                    self.state = "playing"
                return
            elif key == 'h':
                self._show_high_scores()
                return
            elif key == 'q':
                pygame.quit()
                sys.exit()
        
        # Handle button clicks
        for button in self.buttons:
            if button.handle_event(event):
                if button.text == "[N]ew Game":
                    self._start_new_game()
                elif button.text == "[C]ontinue":
                    if self.game.load_game():
                        self.state = "playing"
                elif button.text == "[H]igh Scores":
                    self._show_high_scores()
                elif button.text == "[Q]uit":
                    pygame.quit()
                    sys.exit()
    
    def _handle_playing_event(self, event):
        """Handle gameplay events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self._ask_quit_game():
                self.game.save_high_score()
                self.state = "complete"
                return
        
        if self.input_box:
            if self.input_box.handle_event(event):
                self._submit_answer()
        
        # Handle scroll
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, self.scroll_offset - event.y * 20)
    
    def _handle_complete_event(self, event):
        """Handle game completion events."""
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.state = "menu"
    
    def _update(self, dt):
        """Update game state."""
        if self.input_box:
            self.input_box.update(dt)
    
    def _draw(self):
        """Draw current state."""
        self.screen.fill(COLORS['background'])
        
        if self.state == "welcome":
            self._draw_welcome()
        elif self.state == "menu":
            self._draw_menu()
        elif self.state == "playing":
            self._draw_playing()
        elif self.state == "complete":
            self._draw_complete()
    
    def _draw_welcome(self):
        """Draw welcome screen."""
        # Title
        title = "Python Exception Hierarchy Quiz"
        title_surface, title_rect = self.font_large.render(title, COLORS['primary'])
        title_x = (self.screen.get_width() - title_rect.width) // 2
        self.screen.blit(title_surface, (title_x, 100))
        
        # Rules
        rules = [
            "RULES:",
            "",
            "• View Python code that will raise an exception",
            "• Identify which exception type will be raised",
            "• Type the exact exception name (e.g., 'ValueError')",
            "• Use arrow keys/Tab for autocomplete suggestions",
            "• Progress: Simple → Intermediate → Expert levels",
            "• Higher levels = more points!",
            "",
            "CONTROLS:",
            "• Type your answer and press Enter",
            "• Use ↑↓ or Tab for autocomplete",
            "• Mouse wheel to scroll content",
            "",
            "Good luck and have fun learning!"
        ]
        
        y_offset = 200
        for rule in rules:
            color = COLORS['warning'] if rule.startswith("•") else COLORS['text']
            if rule == "RULES:" or rule == "CONTROLS:":
                color = COLORS['secondary']
            
            rule_surface, rule_rect = self.font_medium.render(rule, color)
            rule_x = (self.screen.get_width() - rule_rect.width) // 2
            self.screen.blit(rule_surface, (rule_x, y_offset))
            y_offset += 30
        
        # Continue prompt
        prompt = "Press any key or click to continue..."
        prompt_surface, prompt_rect = self.font_medium.render(prompt, COLORS['warning'])
        prompt_x = (self.screen.get_width() - prompt_rect.width) // 2
        self.screen.blit(prompt_surface, (prompt_x, y_offset + 50))
    
    def _draw_menu(self):
        """Draw main menu."""
        # Title
        title = "Main Menu"
        title_surface, title_rect = self.font_large.render(title, COLORS['primary'])
        title_x = (self.screen.get_width() - title_rect.width) // 2
        self.screen.blit(title_surface, (title_x, 100))
        
        # Create buttons if not exists
        if not self.buttons:
            button_width = 200
            button_height = 50
            button_x = (self.screen.get_width() - button_width) // 2
            
            buttons_data = [
                ("[N]ew Game", 200),
                ("[C]ontinue", 270) if self.game.has_saved_game() else None,
                ("[H]igh Scores", 340),
                ("[Q]uit", 410)
            ]
            
            self.buttons = []
            for button_data in buttons_data:
                if button_data:
                    text, y = button_data
                    self.buttons.append(Button(button_x, y, button_width, button_height, 
                                             text, self.font_medium))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Add keyboard shortcut instructions
        shortcut_text = "Use keyboard shortcuts: N, C, H, Q or click buttons"
        shortcut_surface, shortcut_rect = self.font_small.render(shortcut_text, COLORS['text_dim'])
        shortcut_x = (self.screen.get_width() - shortcut_rect.width) // 2
        self.screen.blit(shortcut_surface, (shortcut_x, 480))
    
    def _draw_playing(self):
        """Draw gameplay screen."""
        question = self.game.get_current_question()
        if not question:
            return
        
        stats = self.game.get_game_stats()
        difficulty, total_questions = self.game.get_level_info(self.game.current_level)
        
        # Header
        header = (f"Level {self.game.current_level} ({difficulty.title()}) - "
                 f"Question {stats['current_question']}/{total_questions} | "
                 f"Score: {self.game.score}")
        header_surface, header_rect = self.font_medium.render(header, COLORS['secondary'])
        self.screen.blit(header_surface, (20, 20))
        
        # Progress bar
        progress = stats['progress'] / 100
        progress_rect = pygame.Rect(20, 50, self.screen.get_width() - 40, 10)
        pygame.draw.rect(self.screen, COLORS['border'], progress_rect)
        progress_fill = pygame.Rect(20, 50, int((self.screen.get_width() - 40) * progress), 10)
        pygame.draw.rect(self.screen, COLORS['success'], progress_fill)
        
        # Code section
        code_y = 80
        code_title_surface, _ = self.font_medium.render("CODE:", COLORS['warning'])
        self.screen.blit(code_title_surface, (20, code_y))
        
        # Code box
        code_box = pygame.Rect(20, code_y + 30, self.screen.get_width() - 40, 200)
        pygame.draw.rect(self.screen, COLORS['surface'], code_box)
        pygame.draw.rect(self.screen, COLORS['border'], code_box, 2)
        
        # Code text
        code_lines = question['code'].split('\n')
        y_pos = code_box.y + 10 - self.scroll_offset
        
        for line in code_lines:
            if y_pos > code_box.bottom:
                break
            if y_pos + 20 > code_box.y:  # Only draw visible lines
                wrapped_lines = textwrap.wrap(line, 80) if len(line) > 80 else [line]
                for wrapped_line in wrapped_lines:
                    if y_pos > code_box.bottom:
                        break
                    if y_pos + 20 > code_box.y:
                        line_surface, _ = self.font_code.render(wrapped_line, COLORS['text'])
                        self.screen.blit(line_surface, (code_box.x + 10, y_pos))
                    y_pos += 20
            else:
                y_pos += 20
        
        # Context section  
        context_y = code_box.bottom + 20
        context_text = f"Context: {question['context']}"
        context_surface, _ = self.font_medium.render(context_text, COLORS['secondary'])
        self.screen.blit(context_surface, (20, context_y))
        
        # Input section
        input_y = context_y + 50
        input_title_surface, _ = self.font_medium.render("Your answer (start typing):", COLORS['text'])
        self.screen.blit(input_title_surface, (20, input_y))
        
        # Create input box if not exists - make it same width as code box
        if not self.input_box:
            code_box_width = self.screen.get_width() - 40  # Same as code box
            self.input_box = InputBox(20, input_y + 30, code_box_width, 35, self.font_medium)
            self.input_box.set_suggestions(self.game.python_exceptions)
            self.input_box.active = True  # Auto-focus the input box
        
        self.input_box.draw(self.screen)
    
    def _draw_complete(self):
        """Draw game completion screen."""
        stats = self.game.get_game_stats()
        
        # Title
        title = "CONGRATULATIONS!"
        title_surface, title_rect = self.font_large.render(title, COLORS['success'])
        title_x = (self.screen.get_width() - title_rect.width) // 2
        self.screen.blit(title_surface, (title_x, 50))
        
        # Stats
        stats_text = [
            "You've completed the Python Exception Quiz!",
            "",
            f"Final Score: {self.game.score}",
            f"Questions Completed: {stats['completed_questions']}/{stats['total_questions']}",
            f"Accuracy: {stats['progress']:.1f}%"
        ]
        
        y_offset = 120
        for text in stats_text:
            if text:
                text_surface, text_rect = self.font_medium.render(text, COLORS['text'])
                text_x = (self.screen.get_width() - text_rect.width) // 2
                self.screen.blit(text_surface, (text_x, y_offset))
            y_offset += 30
        
        # High scores
        high_scores = self.game.get_high_scores()
        if high_scores:
            scores_title = "HIGH SCORES"
            scores_title_surface, scores_title_rect = self.font_medium.render(scores_title, COLORS['secondary'])
            scores_title_x = (self.screen.get_width() - scores_title_rect.width) // 2
            self.screen.blit(scores_title_surface, (scores_title_x, y_offset + 20))
            
            y_offset += 60
            headers = f"{'Rank':<6}{'Name':<15}{'Score':<10}{'Level':<8}"
            headers_surface, _ = self.font_small.render(headers, COLORS['text_dim'])
            self.screen.blit(headers_surface, (200, y_offset))
            
            y_offset += 25
            for i, score in enumerate(high_scores[:8], 1):
                score_line = f"{i:<6}{score['name']:<15}{score['score']:<10}{score['level_reached']:<8}"
                color = COLORS['warning'] if score['name'] == self.game.player_name else COLORS['text']
                score_surface, _ = self.font_small.render(score_line, color)
                self.screen.blit(score_surface, (200, y_offset))
                y_offset += 20
        
        # Continue prompt
        prompt = "Press any key to return to main menu..."
        prompt_surface, prompt_rect = self.font_medium.render(prompt, COLORS['warning'])
        prompt_x = (self.screen.get_width() - prompt_rect.width) // 2
        self.screen.blit(prompt_surface, (prompt_x, self.screen.get_height() - 50))
    
    def _start_new_game(self):
        """Start a new game."""
        self.game.reset_game()
        
        # Simple name input (could be enhanced with a proper dialog)
        name = self._get_name_input()
        if name:
            self.game.player_name = name
            self.state = "playing"
            self.input_box = None
    
    def _get_name_input(self) -> str:
        """Simple name input screen."""
        name = ""
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        return name.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        name += event.unicode
            
            # Draw name input screen
            self.screen.fill(COLORS['background'])
            
            title = "Enter Your Name"
            title_surface, title_rect = self.font_large.render(title, COLORS['primary'])
            title_x = (self.screen.get_width() - title_rect.width) // 2
            self.screen.blit(title_surface, (title_x, 200))
            
            # Input box - centered like title
            input_width = 400
            input_x = (self.screen.get_width() - input_width) // 2
            input_rect = pygame.Rect(input_x, 300, input_width, 40)
            pygame.draw.rect(self.screen, COLORS['input_bg'], input_rect)
            pygame.draw.rect(self.screen, COLORS['border'], input_rect, 2)
            
            if name:
                name_surface, _ = self.font_medium.render(name, COLORS['text'])
                self.screen.blit(name_surface, (input_rect.x + 10, input_rect.y + 8))
            
            # Prompt
            prompt = "Press Enter when ready"
            prompt_surface, prompt_rect = self.font_medium.render(prompt, COLORS['text_dim'])
            prompt_x = (self.screen.get_width() - prompt_rect.width) // 2
            self.screen.blit(prompt_surface, (prompt_x, 370))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return ""
    
    def _submit_answer(self):
        """Submit the current answer."""
        if not self.input_box:
            return
        
        user_answer = self.input_box.text.strip()
        if not user_answer:
            return
        
        # Check answer
        correct, explanation = self.game.check_answer(user_answer)
        
        # Show result (simple popup for now)
        self._show_result(correct, explanation)
        
        # Reset input and keep focus
        self.input_box.text = ""
        self.input_box.cursor_pos = 0
        self.input_box.active = True  # Keep focus for next question
        self.scroll_offset = 0
        
        # Save progress
        self.game.save_game()
        
        # Move to next question or complete
        if not self.game.next_question():
            self.game.save_high_score()
            self.state = "complete"
    
    def _show_result(self, correct: bool, explanation: str):
        """Show result popup."""
        # Simple result screen - could be enhanced
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            
            # Draw result
            self.screen.fill(COLORS['background'])
            
            if correct:
                result_text = "CORRECT!"
                points = 10 * self.game.current_level
                points_text = f"+{points} points"
                color = COLORS['success']
            else:
                question = self.game.get_current_question()
                result_text = "INCORRECT!"
                points_text = f"Answer: {question['correct_answer'] if question else 'Unknown'}"
                color = COLORS['error']
            
            # Result text
            result_surface, result_rect = self.font_large.render(result_text, color)
            result_x = (self.screen.get_width() - result_rect.width) // 2
            self.screen.blit(result_surface, (result_x, 200))
            
            points_surface, points_rect = self.font_medium.render(points_text, COLORS['warning'])
            points_x = (self.screen.get_width() - points_rect.width) // 2
            self.screen.blit(points_surface, (points_x, 250))
            
            # Explanation
            explanation_lines = textwrap.wrap(explanation, 60)
            y_offset = 300
            for line in explanation_lines:
                line_surface, line_rect = self.font_small.render(line, COLORS['text'])
                line_x = (self.screen.get_width() - line_rect.width) // 2
                self.screen.blit(line_surface, (line_x, y_offset))
                y_offset += 25
            
            # Continue prompt
            prompt = "Press any key to continue..."
            prompt_surface, prompt_rect = self.font_medium.render(prompt, COLORS['text_dim'])
            prompt_x = (self.screen.get_width() - prompt_rect.width) // 2
            self.screen.blit(prompt_surface, (prompt_x, y_offset + 50))
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def _ask_quit_game(self) -> bool:
        """Ask if the player wants to quit the game."""
        waiting = True
        result = False
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        result = True
                        waiting = False
                    elif event.key == pygame.K_n:
                        result = False
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        result = False
                        waiting = False
            
            self.screen.fill(COLORS['background'])
            
            # Title
            title = "Quit Game?"
            title_surface, title_rect = self.font_large.render(title, COLORS['warning'])
            title_x = (self.screen.get_width() - title_rect.width) // 2
            self.screen.blit(title_surface, (title_x, 150))
            
            # Question
            quit_text = [
                "Do you want to quit the current game?",
                "",
                "Your progress will be saved.",
                "You can continue later from where you left off."
            ]
            
            y_offset = 250
            for text in quit_text:
                if text:
                    text_surface, text_rect = self.font_medium.render(text, COLORS['text'])
                    text_x = (self.screen.get_width() - text_rect.width) // 2
                    self.screen.blit(text_surface, (text_x, y_offset))
                y_offset += 35
            
            # Options
            options = "Press 'Y' to Quit, 'N' to Continue Playing"
            options_surface, options_rect = self.font_medium.render(options, COLORS['secondary'])
            options_x = (self.screen.get_width() - options_rect.width) // 2
            self.screen.blit(options_surface, (options_x, y_offset + 30))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return result
    
    def _show_high_scores(self):
        """Show high scores screen."""
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            
            self.screen.fill(COLORS['background'])
            
            # Title
            title = "HIGH SCORES"
            title_surface, title_rect = self.font_large.render(title, COLORS['secondary'])
            title_x = (self.screen.get_width() - title_rect.width) // 2
            self.screen.blit(title_surface, (title_x, 100))
            
            # Scores
            high_scores = self.game.get_high_scores()
            if high_scores:
                headers = f"{'Rank':<6}{'Name':<20}{'Score':<10}{'Level':<8}"
                headers_surface, _ = self.font_medium.render(headers, COLORS['warning'])
                self.screen.blit(headers_surface, (200, 200))
                
                y_offset = 230
                for i, score in enumerate(high_scores[:10], 1):
                    score_line = f"{i:<6}{score['name']:<20}{score['score']:<10}{score['level_reached']:<8}"
                    score_surface, _ = self.font_small.render(score_line, COLORS['text'])
                    self.screen.blit(score_surface, (200, y_offset))
                    y_offset += 25
            else:
                no_scores_surface, no_scores_rect = self.font_medium.render("No high scores yet!", COLORS['text_dim'])
                no_scores_x = (self.screen.get_width() - no_scores_rect.width) // 2
                self.screen.blit(no_scores_surface, (no_scores_x, 250))
            
            # Back prompt
            prompt = "Press any key to go back..."
            prompt_surface, prompt_rect = self.font_medium.render(prompt, COLORS['text_dim'])
            prompt_x = (self.screen.get_width() - prompt_rect.width) // 2
            self.screen.blit(prompt_surface, (prompt_x, self.screen.get_height() - 50))
            
            pygame.display.flip()
            self.clock.tick(60)

def main():
    """Main entry point for pygame version."""
    import argparse
    parser = argparse.ArgumentParser(description="Python Exception Quiz - Pygame GUI Version")
    parser.add_argument('--data-dir', default='data',
                       help='Directory containing game data files')
    args = parser.parse_args()
    
    try:
        gui_game = GUIQuizGame(args.data_dir)
        gui_game.run()
    except pygame.error as e:
        print(f"Pygame error: {e}")
        print("Make sure pygame is installed: pip install pygame")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
