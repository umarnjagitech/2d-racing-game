# 2D Racing Game

A simple 2D first-person racing game built with Pygame, designed to be later ported to Unreal Engine.

![Game Screenshot](images/gameScreenshot1.png)

## Features

- First-person perspective racing
- Simple physics-based car controls
- Custom track with collision detection
- Speedometer and lap timer
- Basic HUD with game information

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

To start the game, run:

```bash
python main.py
```

## Controls

- **Up Arrow / W**: Accelerate
- **Down Arrow / S**: Brake/Reverse
- **Left/Right Arrows / A/D**: Steer
- **ESC**: Quit game

## Project Structure

- `main.py`: Entry point of the game
- `src/`: Source code
  - `core/`: Core game logic
    - `game.py`: Main game loop and state management
    - `car.py`: Player vehicle implementation
    - `track.py`: Track generation and rendering
  - `ui/`: User interface components
    - `hud.py`: Heads-up display
  - `utils/`: Utility functions and constants
    - `constants.py`: Game-wide constants

## Future Improvements

- Add AI opponents
- Implement power-ups and collectibles
- Add sound effects and music
- Improve graphics with better sprites
- Add different game modes
- Port to Unreal Engine for 3D version

## Version 1.1: Side-Scrolling Update (Planned)

### New Features
- **Lane-Based Gameplay**: Cars move left-to-right or right-to-left in designated lanes
- **Multiple Tracks**: Varied environments including city, desert, and mountain themes
- **Enhanced Vehicle Models**: Detailed car sprites with different models and colors
- **Track Features**:
  - Multiple lanes (2-4) for strategic overtaking
  - Traffic cars moving in both directions
  - Environmental hazards and obstacles
  - Checkpoints and finish lines
- **Game Modes**:
  - Time trial
  - Career mode with progressive difficulty
  - Endless mode

### Technical Improvements
- Redesigned car physics for side-scrolling
- Dynamic track generation
- Improved collision detection
- Optimized performance for smooth scrolling

### Future Expansion
- Multiplayer support (local/online)
- Power-ups and special abilities
- Customization options for vehicles
- More tracks and environments

## License

This project is open source and available under the MIT License.
