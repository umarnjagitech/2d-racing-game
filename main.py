#!/usr/bin/env python3
# 2D First-Person Racing Game
# Main entry point for the game
import sys
import pygame
from src.core.game import RacingGame

def main():
    # Initialize and run the game
    try:
        game = RacingGame("2D Racing Game", 1200, 800)
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
