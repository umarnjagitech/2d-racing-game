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

## License

This project is open source and available under the MIT License.
