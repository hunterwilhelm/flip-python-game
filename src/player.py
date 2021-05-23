import arcade

from src.constants import CHARACTER_SCALING

_TEXTURE_RIGHT = 0
_TEXTURE_LEFT = 1


class Player(arcade.Sprite):
    """ My custom player """

    def __init__(self, texture_name: str, scale: float):
        super().__init__(scale=scale)

        # settings
        self.scale = CHARACTER_SCALING
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        self.textures.append(arcade.load_texture(texture_name))
        self.textures.append(arcade.load_texture(texture_name, flipped_horizontally=True))

        # state
        self._goingRight = True
        # By default, face right.
        self.texture = self.textures[_TEXTURE_RIGHT]

    def update(self):
        """ Animate the player. The physics engine does the movement """
        # Figure out if we should face left or right
        if self.change_x < 0:
            self._update_texture(False)
        elif self.change_x > 0:
            self._update_texture(True)

    def _update_texture(self, goingRight):
        """ Only update the texture if it needs to be changed """
        if self._goingRight != goingRight:
            if goingRight:
                self.texture = self.textures[_TEXTURE_RIGHT]
            else:
                self.texture = self.textures[_TEXTURE_LEFT]
        self._goingRight = goingRight

    def face_other_way(self):
        """ Used for the flip animation since we are rotating the entire screen """
        self._update_texture(not self._goingRight)
