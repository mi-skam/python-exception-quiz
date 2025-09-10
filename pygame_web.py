#!/usr/bin/env python3
"""
Python Exception Quiz - Pygame Web Version
Async-compatible version for browser deployment using pygbag
"""

import pygame
import pygame.freetype
import sys
import os
import asyncio
import textwrap
from typing import List, Optional, Tuple

# Import game engine - handle both development and package modes
try:
    from src.python_exception_quiz.game_engine import ExceptionQuizGame
except ImportError:
    try:
        from game_engine import ExceptionQuizGame
    except ImportError:
        print("Error: Could not import game engine. Make sure the project structure is correct.")
        sys.exit(1)

# Colors (same as desktop version)
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
            if self.rect.collidepoint(event.pos):
                self.active = True
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
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
        if self.cursor_timer >= 500:
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

class WebGUIQuizGame:
    """Web-compatible Pygame GUI for the Exception Quiz Game."""
    
    def __init__(self, data_dir: str = "data"):
        pygame.init()
        pygame.freetype.init()
        
        # Smaller screen size for web compatibility
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Python Exception Hierarchy Quiz")
        
        # Load fonts with web-compatible fallbacks
        try:
            self.font_code = pygame.freetype.SysFont('monospace', 16)
        except:
            self.font_code = pygame.freetype.Font(None, 16)
            
        self.font_large = pygame.freetype.Font(None, 28)
        self.font_medium = pygame.freetype.Font(None, 20)
        self.font_small = pygame.freetype.Font(None, 16)
        
        self.clock = pygame.time.Clock()
        
        # Initialize game engine with error handling
        try:
            self.game = ExceptionQuizGame(data_dir)
        except Exception as e:
            print(f"Warning: Could not load game data: {e}")
            # Create a minimal game instance for web demo
            self.game = None
        
        self.data_dir = data_dir
        
        # Game state
        self.state = "welcome"
        self.input_box = None
        self.buttons = []
        self.scroll_offset = 0
        
        # Web-specific settings
        self.running = True
    
    async def run(self):
        """Async main game loop for web compatibility."""
        while self.running:
            dt = self.clock.tick(60)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self._handle_event(event)
            
            # Update
            self._update(dt)
            
            # Draw
            self._draw()
            
            pygame.display.flip()
            
            # Required for web - yield control to browser
            await asyncio.sleep(0)
        
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
        if event.type == pygame.KEYDOWN:
            key = event.unicode.lower() if event.unicode else None
            
            if key == 'n':
                self._start_new_game()
                return
            elif key == 'c' and self.game and self.game.has_saved_game():
                if self.game.load_game():
                    self.state = "playing"
                return
            elif key == 'h':
                self._show_high_scores()
                return
            elif key == 'q':
                self.running = False
        
        # Handle button clicks
        for button in self.buttons:
            if button.handle_event(event):
                if button.text == "[N]ew Game":
                    self._start_new_game()
                elif button.text == "[C]ontinue":
                    if self.game and self.game.load_game():
                        self.state = "playing"
                elif button.text == "[H]igh Scores":
                    self._show_high_scores()
                elif button.text == "[Q]uit":
                    self.running = False
    
    def _handle_playing_event(self, event):
        """Handle gameplay events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self._ask_quit_game():
                if self.game:
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
        title = "Python Exception Quiz"
        title_surface, title_rect = self.font_large.render(title, COLORS['primary'])
        title_x = (self.screen.get_width() - title_rect.width) // 2
        self.screen.blit(title_surface, (title_x, 50))
        
        rules = [
            "🐍 Web Version - Learn Python Exceptions! 🐍",
            "",
            "• View code that raises exceptions",
            "• Identify the exception type", 
            "• Type exact names (e.g., 'ValueError')",
            "• Use Tab/arrows for autocomplete",
            "",
            "Controls: Type answer → Enter",
            "",
            "Click or press any key to start!"
        ]
        
        y_offset = 120
        for rule in rules:
            color = COLORS['warning'] if rule.startswith("•") else COLORS['text']
            if "🐍" in rule:
                color = COLORS['success']
            elif rule.startswith("Controls"):
                color = COLORS['secondary']
            
            rule_surface, rule_rect = self.font_small.render(rule, color)
            rule_x = (self.screen.get_width() - rule_rect.width) // 2
            self.screen.blit(rule_surface, (rule_x, y_offset))
            y_offset += 25
    
    def _draw_menu(self):
        """Draw main menu."""
        title = "Main Menu"
        title_surface, title_rect = self.font_large.render(title, COLORS['primary'])
        title_x = (self.screen.get_width() - title_rect.width) // 2
        self.screen.blit(title_surface, (title_x, 80))
        
        # Create buttons if not exists
        if not self.buttons:
            button_width = 180
            button_height = 40
            button_x = (self.screen.get_width() - button_width) // 2
            
            buttons_data = [
                ("[N]ew Game", 150),
                ("[C]ontinue", 200) if self.game and self.game.has_saved_game() else None,
                ("[H]igh Scores", 250),
                ("[Q]uit", 300)
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
        
        # Instructions
        shortcut_text = "Keyboard: N, C, H, Q"
        shortcut_surface, shortcut_rect = self.font_small.render(shortcut_text, COLORS['text_dim'])
        shortcut_x = (self.screen.get_width() - shortcut_rect.width) // 2
        self.screen.blit(shortcut_surface, (shortcut_x, 360))
    
    def _draw_playing(self):
        """Draw gameplay screen."""
        if not self.game:
            # Show demo message if game couldn't load
            demo_text = "Demo Mode - Game data not available"
            demo_surface, demo_rect = self.font_medium.render(demo_text, COLORS['warning'])
            demo_x = (self.screen.get_width() - demo_rect.width) // 2
            self.screen.blit(demo_surface, (demo_x, 200))
            return
        
        question = self.game.get_current_question()
        if not question:
            return
        
        stats = self.game.get_game_stats()
        difficulty, total_questions = self.game.get_level_info(self.game.current_level)
        
        # Compact header for web
        header = f"L{self.game.current_level} ({difficulty}) - Q{stats['current_question']}/{total_questions} | Score: {self.game.score}"
        header_surface, header_rect = self.font_small.render(header, COLORS['secondary'])
        self.screen.blit(header_surface, (10, 10))
        
        # Progress bar
        progress = stats['progress'] / 100
        progress_rect = pygame.Rect(10, 30, self.screen.get_width() - 20, 8)
        pygame.draw.rect(screen, COLORS['border'], progress_rect)
        progress_fill = pygame.Rect(10, 30, int((self.screen.get_width() - 20) * progress), 8)
        pygame.draw.rect(self.screen, COLORS['success'], progress_fill)
        
        # Code section
        code_y = 50
        code_title_surface, _ = self.font_medium.render("CODE:", COLORS['warning'])
        self.screen.blit(code_title_surface, (10, code_y))
        
        # Compact code box for web
        code_box = pygame.Rect(10, code_y + 25, self.screen.get_width() - 20, 180)
        pygame.draw.rect(self.screen, COLORS['surface'], code_box)
        pygame.draw.rect(self.screen, COLORS['border'], code_box, 2)
        
        # Code text
        code_lines = question['code'].split('\n')
        y_pos = code_box.y + 8 - self.scroll_offset
        
        for line in code_lines:
            if y_pos > code_box.bottom:
                break
            if y_pos + 16 > code_box.y:
                # Wrap long lines for web
                wrapped_lines = textwrap.wrap(line, 70) if len(line) > 70 else [line]
                for wrapped_line in wrapped_lines:
                    if y_pos > code_box.bottom:
                        break
                    if y_pos + 16 > code_box.y:
                        line_surface, _ = self.font_code.render(wrapped_line, COLORS['text'])
                        self.screen.blit(line_surface, (code_box.x + 8, y_pos))
                    y_pos += 16
            else:
                y_pos += 16
        
        # Context section
        context_y = code_box.bottom + 10
        context_text = f"Context: {question['context']}"
        # Wrap context for web
        context_wrapped = textwrap.wrap(context_text, 60)
        for i, line in enumerate(context_wrapped):
            context_surface, _ = self.font_small.render(line, COLORS['secondary'])
            self.screen.blit(context_surface, (10, context_y + i * 18))
        
        # Input section  
        input_y = context_y + len(context_wrapped) * 18 + 20
        input_title_surface, _ = self.font_medium.render("Your answer:", COLORS['text'])
        self.screen.blit(input_title_surface, (10, input_y))
        
        # Create input box if not exists
        if not self.input_box:
            input_width = self.screen.get_width() - 20
            self.input_box = InputBox(10, input_y + 25, input_width, 30, self.font_medium)
            if self.game:
                self.input_box.set_suggestions(self.game.python_exceptions)
            self.input_box.active = True
        
        self.input_box.draw(self.screen)
    
    def _draw_complete(self):
        """Draw game completion screen."""
        title = "Complete!"
        title_surface, title_rect = self.font_large.render(title, COLORS['success'])
        title_x = (self.screen.get_width() - title_rect.width) // 2
        self.screen.blit(title_surface, (title_x, 100))
        
        if self.game:
            stats = self.game.get_game_stats()
            stats_text = [
                f"Final Score: {self.game.score}",
                f"Questions: {stats['completed_questions']}/{stats['total_questions']}",
                f"Accuracy: {stats['progress']:.1f}%"
            ]
            
            y_offset = 200
            for text in stats_text:
                text_surface, text_rect = self.font_medium.render(text, COLORS['text'])
                text_x = (self.screen.get_width() - text_rect.width) // 2
                self.screen.blit(text_surface, (text_x, y_offset))
                y_offset += 30
        
        # Continue prompt
        prompt = "Click or press any key for menu..."
        prompt_surface, prompt_rect = self.font_small.render(prompt, COLORS['text_dim'])
        prompt_x = (self.screen.get_width() - prompt_rect.width) // 2
        self.screen.blit(prompt_surface, (prompt_x, 400))
    
    def _start_new_game(self):
        """Start a new game."""
        if not self.game:
            return
            
        self.game.reset_game()
        self.game.player_name = "WebPlayer"  # Simple name for web
        self.state = "playing"
        self.input_box = None
    
    def _submit_answer(self):
        """Submit the current answer."""
        if not self.input_box or not self.game:
            return
        
        user_answer = self.input_box.text.strip()
        if not user_answer:
            return
        
        # Check answer
        correct, explanation = self.game.check_answer(user_answer)
        
        # Simple result feedback for web
        self.input_box.text = "✓ Correct!" if correct else f"✗ Wrong: {self.game.get_current_question()['correct_answer']}"
        
        # Brief pause, then continue
        pygame.time.wait(1000)
        
        # Reset input
        self.input_box.text = ""
        self.input_box.cursor_pos = 0
        self.input_box.active = True
        self.scroll_offset = 0
        
        # Save and move to next
        self.game.save_game()
        if not self.game.next_question():
            self.game.save_high_score()
            self.state = "complete"
    
    def _ask_quit_game(self) -> bool:
        """Simple quit confirmation for web."""
        return True  # Simplified for web
    
    def _show_high_scores(self):
        """Show high scores (simplified for web)."""
        # For web version, just return to menu quickly
        pass

async def main():
    """Async main entry point for web version."""
    try:
        # Try to detect data directory
        data_dir = "data"
        if not os.path.exists(data_dir):
            # Try alternative paths for web deployment
            for alt_dir in ["./data", "../data", "src/data"]:
                if os.path.exists(alt_dir):
                    data_dir = alt_dir
                    break
        
        gui_game = WebGUIQuizGame(data_dir)
        await gui_game.run()
        
    except Exception as e:
        print(f"Error running web game: {e}")
        print("This is the web version - some features may be limited")

# Entry point for pygbag
if __name__ == "__main__":
    asyncio.run(main())