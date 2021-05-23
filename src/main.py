"""
Python Flip Game

Hunter Wilhelm


Artwork in the game from:
https://craftpix.net/file-licenses/

Paying my dues:
This was inspired by the SHIFT game
SHIFT was developed and published by Armor Games
Anthony Lavelle created the concept, design, and did the programming
Full credits in the game on Armor Games here: https://armorgames.com/play/751/shift
"""
import arcade

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from src.views.instruction_view import InstructionView



def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()



if __name__ == "__main__":
    main()
