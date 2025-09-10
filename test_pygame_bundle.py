#!/usr/bin/env python3
"""Test pygame font loading in bundle."""

import pygame
import pygame.freetype
import sys
import traceback

print("Testing pygame font loading...")

try:
    pygame.init()
    print("✓ pygame.init() successful")
    
    pygame.freetype.init()
    print("✓ pygame.freetype.init() successful")
    
    # Test 1: Default font
    try:
        font1 = pygame.freetype.Font(None, 20)
        print("✓ pygame.freetype.Font(None, 20) successful")
    except Exception as e:
        print(f"✗ pygame.freetype.Font(None, 20) failed: {e}")
        traceback.print_exc()
    
    # Test 2: System font
    try:
        font2 = pygame.freetype.SysFont('monospace', 20)
        print("✓ pygame.freetype.SysFont('monospace', 20) successful")
    except Exception as e:
        print(f"✗ pygame.freetype.SysFont('monospace', 20) failed: {e}")
    
    # Test 3: Regular pygame font (not freetype)
    try:
        font3 = pygame.font.Font(None, 20)
        print("✓ pygame.font.Font(None, 20) successful")
    except Exception as e:
        print(f"✗ pygame.font.Font(None, 20) failed: {e}")
        
    print("\nPython path:", sys.path)
    print("Frozen?", getattr(sys, 'frozen', False))
    if hasattr(sys, '_MEIPASS'):
        print("Bundle path:", sys._MEIPASS)
        
except Exception as e:
    print(f"Error during testing: {e}")
    traceback.print_exc()