# This file is to store all of the constant variables
# One of the advantages of doing this is to avoid circular dependencies

# Window properties
BLOCK_SIZE = 64
SCREEN_WIDTH = 12 * BLOCK_SIZE
SCREEN_HEIGHT = 12 * BLOCK_SIZE
VIEW_HEIGHT = SCREEN_HEIGHT + BLOCK_SIZE * 2
VIEW_WIDTH = SCREEN_WIDTH + BLOCK_SIZE * 2
SCREEN_TITLE = "Flip Game"

# Scaling
CHARACTER_SCALING = 1

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = .5
PLAYER_JUMP_SPEED = 9
TILE_SCALING = 1

# Animations
WINDOW_FLIP_ANIMATION_DURATION = .5
WINDOW_FLIP_ANIMATION_SCALE = .5
SPRITE_FLIP_ANIMATION_DURATION = 1

# Status
MAX_LEVEL = 2
