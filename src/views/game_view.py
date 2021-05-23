import arcade

from src.constants import *
from src.views.flip_animation_view import FlipAnimationView
from src.player import Player
from src.utils import bezier
from src.views.win_view import WinView


class GameView(arcade.View):
    """
    This is the view that holds all of the game logic
    and displays the game as well.
    """

    """#################### SETUP ####################"""

    def __init__(self):
        super().__init__()

        # state
        self.level = 0
        self.flipped = False
        self.controls_disabled = False

        # animation
        self.sprite_flip_bottom_y = None
        self.sprite_flip_height = None
        self.sprite_flip_start = False
        self.sprite_flip_time = 0

        self.window_flip_start = False

        # Sprites
        self.block_list = None
        self.door_list = None
        self.background_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite: Player = None

        # Better Controls
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Our 'physics' engine
        self.physics_engine = None

        # Level files
        self.level_starting_position = [
            (3 * BLOCK_SIZE / 2, VIEW_HEIGHT / 2 + BLOCK_SIZE * 2),
            (3 * BLOCK_SIZE / 2, VIEW_HEIGHT / 2),
        ]
        self.level_maps = [
            "assets/maps/level1.tmx",
            "assets/maps/level2.tmx",
        ]
        self.flipped_level_maps = [
            "assets/maps/level1flipped.tmx",
            "assets/maps/level2flipped.tmx",
        ]

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        arcade.set_background_color(arcade.color.WHITE)

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()

        # Create your sprites and sprite lists
        image_source = "assets/sprites/monster_owlet/Owlet_Monster.png"
        self.player_sprite = Player(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = self.level_starting_position[self.level][0]
        self.player_sprite.center_y = self.level_starting_position[self.level][1]
        self.player_list.append(self.player_sprite)

        # Name of map file to load
        # Name of the layer in the file that has our platforms/walls
        self.update_map_platform(self.level_maps[0])

    def on_resume_after_flip(self):
        """ This is called by FlipAnimationView and it is like setup for after the flip animation """

        # hide border blocks
        arcade.set_viewport(BLOCK_SIZE, SCREEN_WIDTH + BLOCK_SIZE, BLOCK_SIZE, SCREEN_HEIGHT + BLOCK_SIZE)

        # this function is called on the first go, so no need to flip
        if self.sprite_flip_start or self.window_flip_start:
            self.flipped = not self.flipped

            # set flipped map
            if self.flipped:
                map_name = self.flipped_level_maps[self.level]
            else:
                map_name = self.level_maps[self.level]
            self.update_map_platform(map_name)

            # allow the player to play again
            self.enable_controls()

            # reset state
            self.sprite_flip_start = False
            self.window_flip_start = False

    """#################### EVENTS ####################"""

    def on_draw(self):
        """ Render the screen. """

        # Move focus to another class to do this animation
        if self.window_flip_start:
            flip_view = FlipAnimationView(
                arcade.csscolor.WHITE,
                self,
                animation_duration_after=0,
                middleX=VIEW_HEIGHT / 2,
                middleY=VIEW_WIDTH / 2
            )
            self.window.show_view(flip_view)
            return

        # Refresh page
        arcade.start_render()

        self.block_list.draw()
        self.door_list.draw()
        self.background_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Flip the sprite before the window flip
        if self.sprite_flip_start:
            if not self.window_flip_start:
                self.do_sprite_animation(delta_time)
            return

        # Animate the player
        self.player_list.update()

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Jump code
        if self.up_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        # Move the player with the physics engine
        self.physics_engine.update()

        # Check if the player has completed the level
        if arcade.check_for_collision_with_list(self.player_sprite, self.door_list):
            self.go_to_next_level()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.controls_disabled:
            return

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            if self.physics_engine.can_jump():
                self.start_flip_animation()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    """#################### ACTIONS ####################"""

    def start_flip_animation(self):
        """ This initializes the flip animation process """

        self.disable_controls()
        self.sprite_flip_start = True
        self.sprite_flip_bottom_y = self.player_sprite.center_y - self.player_sprite.height / 2
        self.sprite_flip_height = self.player_sprite.height
        self.sprite_flip_time = 0

    def update_map_platform(self, map_name):
        """ Called on setup and after flipping """
        my_map = arcade.tilemap.read_tmx(map_name)

        def get_platform_list(name: str) -> arcade.SpriteList:
            return arcade.tilemap.process_layer(map_object=my_map,
                                                layer_name=name,
                                                scaling=TILE_SCALING,
                                                use_spatial_hash=True)

        self.door_list = get_platform_list("Doors")
        self.block_list = get_platform_list("Blocks")
        self.background_list = get_platform_list("Background")

        # Create the physics engine

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.block_list,
                                                             gravity_constant=GRAVITY)

    def do_sprite_animation(self, delta_time):
        """ This does the sprite flip animation """

        # Animation clock
        self.sprite_flip_time += delta_time

        # For a limited time, flip the character using the ease in and out style.
        if self.sprite_flip_time < SPRITE_FLIP_ANIMATION_DURATION:
            self.flip_player(self.sprite_flip_time / SPRITE_FLIP_ANIMATION_DURATION)
        else:
            # reset the player
            self.flip_player(0)
            self.player_sprite.face_other_way()

            # move player to flipped position
            self.player_sprite.center_y = VIEW_HEIGHT - self.player_sprite.center_y + self.player_sprite.height
            self.player_sprite.center_x = VIEW_WIDTH - self.player_sprite.center_x

            # allow the window flip to start
            self.window_flip_start = True

    def flip_player(self, progress: float):
        """ This does the sprite flip calculation """

        y_scale = 1 - 2 * bezier(progress)
        self.player_sprite.height = (y_scale * self.sprite_flip_height)
        self.player_sprite.center_y = self.sprite_flip_bottom_y + self.player_sprite.height / 2

    def disable_controls(self):
        """ User is not allowed to move while the animations are happening """

        self.down_pressed = False
        self.up_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.controls_disabled = True

    def enable_controls(self):
        """ Once the animations are done, this allows the user to control the player again """

        self.controls_disabled = False

    def go_to_next_level(self):
        """ Once the user has touched the door, then move to the next level """

        self.level += 1
        if self.level < MAX_LEVEL:
            self.update_map_platform(self.level_maps[self.level])
            self.player_sprite.center_x = self.level_starting_position[self.level][0]
            self.player_sprite.center_y = self.level_starting_position[self.level][1]
        else:
            view = WinView()
            self.window.show_view(view)
