import arcade

from src.constants import TILE_SCALING, CHARACTER_SCALING, GRAVITY, PLAYER_JUMP_SPEED, PLAYER_MOVEMENT_SPEED, \
    SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_FLIP_ANIMATION_DURATION
from src.flip_animation_view import FlipAnimationView
from src.player import Player
from src.utils import bezier


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()
        # state
        self.flipped = False

        # helpers
        self.sprite_flip_bottom_y = None
        self.sprite_flip_height = None
        self.controls_disabled = False

        # animation
        self.sprite_flip_start = False
        self.sprite_flip_time = 0

        self.window_flip_start = False

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

        self.stars = None

        self.level_maps = [
            "assets/maps/level1.tmx"
        ]
        self.flipped_level_maps = [
            "assets/maps/level1flipped.tmx"
        ]

    def update_map_platform(self, map_name):
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

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        arcade.set_background_color(arcade.color.WHITE)

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()

        # --- Load in a map from the tiled editor ---

        # Create your sprites and sprite lists here
        image_source = "assets/sprites/monster_owlet/Owlet_Monster.png"
        self.player_sprite = Player(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 1000
        self.player_list.append(self.player_sprite)

        # Name of map file to load
        # Name of the layer in the file that has our platforms/walls
        self.update_map_platform(self.level_maps[0])

    def on_draw(self):
        """
        Render the screen.
        """
        if self.window_flip_start:
            flip_view = FlipAnimationView(arcade.csscolor.WHITE, self, animation_duration_after=0)
            self.window.show_view(flip_view)
            return

        arcade.start_render()

        self.block_list.draw()
        self.door_list.draw()
        self.background_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.player_list.update()

        if self.sprite_flip_start:
            if not self.window_flip_start:
                self.do_sprite_animation(delta_time)
            return

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if self.up_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        # Move the player with the physics engine
        self.physics_engine.update()

    def do_sprite_animation(self, delta_time):
        self.sprite_flip_time += delta_time
        if self.sprite_flip_time < SPRITE_FLIP_ANIMATION_DURATION:
            y_scale = 1 - 2 * bezier(self.sprite_flip_time / SPRITE_FLIP_ANIMATION_DURATION)
            self.flip_player(y_scale)
        else:
            self.flip_player(1)
            # move player to flipped position
            self.player_sprite.center_y = SCREEN_HEIGHT - self.player_sprite.center_y + self.player_sprite.height
            self.player_sprite.center_x = SCREEN_WIDTH - self.player_sprite.center_x

            self.player_sprite.face_other_way()
            self.window_flip_start = True

    def flip_player(self, y_scale: float):
        self.player_sprite.height = (y_scale * self.sprite_flip_height)
        self.player_sprite.center_y = self.sprite_flip_bottom_y + self.player_sprite.height / 2

    def on_resume_after_flip(self):
        if self.sprite_flip_start or self.window_flip_start:
            self.flipped = not self.flipped
            if self.flipped:
                map_name = "assets/maps/level1flipped.tmx"
            else:
                map_name = "assets/maps/level1.tmx"
            self.update_map_platform(map_name)
            self.enable_controls()

            self.sprite_flip_start = False
            self.window_flip_start = False

    def disable_controls(self):
        self.down_pressed = False
        self.up_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.controls_disabled = True

    def enable_controls(self):
        self.controls_disabled = False

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.controls_disabled:
            return

        if key == arcade.key.UP or key == arcade.key.W:
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

    def start_flip_animation(self):
        self.disable_controls()
        self.sprite_flip_start = True
        self.sprite_flip_bottom_y = self.player_sprite.center_y - self.player_sprite.height / 2
        self.sprite_flip_height = self.player_sprite.height
        self.sprite_flip_time = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
