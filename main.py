#!/usr/bin/env python3
# 2D First-Person Racing Game
# Main entry point for the game
import sys
import os
import pygame

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

print("Starting game...")
print(f"Python version: {sys.version}")
print(f"Pygame version: {pygame.version.ver if hasattr(pygame, 'version') else 'Unknown'}")

from core.game import RacingGame

def main():
    # Initialize and run the game
    try:
        print("Initializing game...")
        game = RacingGame("2D Racing Game", 1200, 800)
        print("Game initialized. Starting game loop...")
        game.run()
        print("Game loop ended.")
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0

if __name__ == "__main__":
    print("Starting main function...")
    sys.exit(main())
