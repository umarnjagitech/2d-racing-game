# Project Specification: 2D Racing Game

## Code Style and Naming Conventions

### Python Code
- **PEP 8** compliance (4-space indentation, 79/88 character line length)
- **Class Names**: `PascalCase`
- **Function/Method Names**: `snake_case`
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private Members**: `_leading_underscore`
- **Type Hints**: Required for all function/method parameters and return values
- **Docstrings**: Google style docstrings for all public classes and functions

### File Structure
```
racing_game/
│
├── assets/                 # Game assets (images, sounds, fonts)
│   ├── images/            # Image assets
│   ├── sounds/            # Sound effects and music
│   └── fonts/             # Font files
│
├── data/                  # Game data files
│   ├── tracks/            # Track definitions
│   └── savegames/         # Player save data
│
├── src/                   # Source code
│   ├── core/              # Core game logic
│   │   ├── __init__.py
│   │   ├── game.py       # Main game class
│   │   ├── car.py        # Player vehicle
│   │   └── track.py      # Track management
│   │
│   ├── ui/                # User interface
│   │   ├── __init__.py
│   │   └── hud.py        # Heads-up display
│   │
│   └── utils/             # Utilities
│       ├── __init__.py
│       └── constants.py  # Game constants
│
├── tests/                 # Unit and integration tests
│   ├── __init__.py
│   ├── test_car.py
│   └── test_track.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

## Development Workflow

### Branching Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/`: Feature branches (e.g., `feature/add-powerups`)
- `bugfix/`: Bug fix branches
- `release/`: Release preparation branches

### Commit Message Format
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code changes that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Changes to the build process or auxiliary tools

## Testing
- Unit tests for all core functionality
- Integration tests for game systems
- Test coverage target: 80%+

## Documentation
- Inline documentation for all public APIs
- README with setup and usage instructions
- Architecture decision records (ADRs) for major decisions

## Dependencies
- Python 3.8+
- Pygame 2.5.2
- Numpy (for future physics)
