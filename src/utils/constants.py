""
Game-wide constants and configuration settings.
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Game settings
GAME_TITLE = "2D Racing Game"

# Car settings
CAR_ACCELERATION = 0.2
CAR_MAX_SPEED = 10
CAR_ROTATION_SPEED = 0.05
CAR_FRICTION = 0.95

# Track settings
TRACK_WIDTH = 800
TRACK_HEIGHT = 600
TRACK_COLOR = (139, 69, 19)  # Brown
GRASS_COLOR = (34, 139, 34)   # Forest green

# Physics
GRAVITY = 0.5

# HUD settings
HUD_FONT_SIZE = 24
HUD_SMALL_FONT_SIZE = 18
HUD_TEXT_COLOR = WHITE
HUD_SPEED_COLOR = GREEN
HUD_WARNING_COLOR = RED

# Input settings
INPUT_DEADZONE = 0.1  # For gamepad support (not implemented yet)
