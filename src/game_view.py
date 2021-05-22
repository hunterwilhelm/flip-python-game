import arcade

from src.constants import TILE_SCALING, CHARACTER_SCALING, GRAVITY, PLAYER_JUMP_SPEED, PLAYER_MOVEMENT_SPEED


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.WHITE)

        self.wall_list = None
        self.coin_list = None
        self.player_list = None
        self.ladder_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Better Controls
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Our 'physics' engine
        self.physics_engine = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()

        # --- Load in a map from the tiled editor ---

        # Name of map file to load
        map_name = "assets/maps/map.tmx"
        # map_name = ":resources:tmx_maps/map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        coins_layer_name = 'Coins'
        self.coin_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=coins_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        # Create your sprites and sprite lists here
        image_source = "assets/sprites/monster_owlet/Owlet_Monster.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 1000
        self.player_list.append(self.player_sprite)

        # Create the physics engine

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY,
                                                             ladders=self.ladder_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # Clear the screen to the background color
        arcade.start_render()

        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Move the player with the physics engine
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
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
