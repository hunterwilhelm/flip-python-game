import arcade

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.flip_animation_view import FlipAnimationView
from src.game_view import GameView


class InstructionView(arcade.View):
    """ View to show instructions """

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Flip", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Goal: get to the green", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Tip: Flip using shift.", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 120,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("To continue, press shift.", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 175,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        """ If the user presses the mouse button, start the game. """
        if modifiers & arcade.key.MOD_SHIFT:
            game_view = GameView()
            game_view.setup()
            flip_view = FlipAnimationView(arcade.csscolor.BLACK, game_view)
            self.window.show_view(flip_view)
