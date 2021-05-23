import arcade

from src.constants import CHARACTER_SCALING

TEXTURE_RIGHT = 0
TEXTURE_LEFT = 1


class Player(arcade.Sprite):

    def __init__(self, texture_name: str, scale: float):
        super().__init__(scale=scale)
        self._goingRight = True

        self.scale = CHARACTER_SCALING
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        self.textures.append(arcade.load_texture(texture_name))
        self.textures.append(arcade.load_texture(texture_name, flipped_horizontally=True))

        # By default, face right.
        self.texture = self.textures[TEXTURE_RIGHT]

    def update(self):
        # Figure out if we should face left or right
        if self.change_x < 0:
            self._update_texture(False)
        elif self.change_x > 0:
            self._update_texture(True)

    def _update_texture(self, goingRight):
        if self._goingRight != goingRight:
            if goingRight:
                self.texture = self.textures[TEXTURE_RIGHT]
            else:
                self.texture = self.textures[TEXTURE_LEFT]
        self._goingRight = goingRight

    def face_other_way(self):
        self._update_texture(not self._goingRight)

