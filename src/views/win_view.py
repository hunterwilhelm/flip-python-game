import arcade

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.views.flip_animation_view import FlipAnimationView
import src.views.instruction_view as instruction_view


class WinView(arcade.View):
    """ View to show that the user has won the game """

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("You have won Flip!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Enjoy your life.", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 120,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("To restart, press shift.", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 175,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        """ If the user presses the mouse button, restart the game. """
        if modifiers & arcade.key.MOD_SHIFT:
            view = instruction_view.InstructionView()
            flip_view = FlipAnimationView(arcade.csscolor.BLACK, view)
            self.window.show_view(flip_view)
