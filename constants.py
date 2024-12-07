WIDTH, HEIGHT = 1920, 1080
FULLSCREEN = False
NUM_STARS = 100
PLAYER_SPEED = 2000
DEPTH_RATE = 0.1
MIN_DEPTH = 0.1
MAX_DEPTH = 1.0
BULLET_MAX_DEPTH = 5.0
STAR_COLOR = (255, 255, 255)
TARGET_COLOR = (255, 0, 0)
# Speed modifiers for bullet types
NEUTRAL_BULLET_SPEED_MOD = 1  # 50% of the original distance for 2D bullets
INWARD_BULLET_SPEED_MOD = 1.0   # Full distance for inward-moving bullets
OUTWARD_BULLET_SPEED_MOD = 1.0  # Full distance for outward-moving bullets

BASE_DIRECTION_MAP = {
    (0, -1): "up",
    (0, 1): "down",
    (-1, 0): "left",
    (1, 0): "right",
    (1, -1): "up-right",
    (-1, -1): "up-left",
    (1, 1): "down-right",
    (-1, 1): "down-left"
}

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "up-right": (1, -1),
    "up-left": (-1, -1),
    "down-right": (1, 1),
    "down-left": (-1, 1),
}
