import arcade
from arcade import Texture, Color

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_FLIP_ANIMATION_DURATION, WINDOW_FLIP_ANIMATION_SCALE
from src.utils import bezier


class FlipAnimationView(arcade.View):
    """ This does the window flip animation between views """

    def __init__(self,
                 backgroundColor: Color,
                 destination_view: arcade.View,
                 animation_duration_after: float = .5,
                 middleX=SCREEN_WIDTH / 2,
                 middleY=SCREEN_HEIGHT / 2):
        super().__init__()
        self.background_color = backgroundColor
        self.destination_view = destination_view
        self.animation_duration_after = animation_duration_after
        self.middleX = middleX
        self.middleY = middleY

        # state
        self.angle = 0
        self.animation_time = 0
        self.load_animation = True
        self.show_animation = False
        self.my_texture: Texture = None

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(self.background_color)
        if self.show_animation:
            self.my_texture.draw_scaled(self.middleX, self.middleY, angle=self.angle, scale=WINDOW_FLIP_ANIMATION_SCALE)

    def on_update(self, delta_time: float):
        if self.load_animation:
            # take a screenshot and assign it to a texture
            image = arcade.get_image()
            self.my_texture = Texture("Background", image)

            # set the state
            self.load_animation = False
            self.show_animation = True
            self.animation_time = 0
        elif self.show_animation:

            # calculate the animation
            self.animation_time += delta_time
            if self.animation_time < WINDOW_FLIP_ANIMATION_DURATION:

                # go from 0 to 180 degrees
                self.angle = 180 * bezier(self.animation_time / WINDOW_FLIP_ANIMATION_DURATION)

                # when it is close enough to 180, snap to it
                if abs(self.angle - 180) < 2:
                    self.angle = 180
            elif self.animation_time > WINDOW_FLIP_ANIMATION_DURATION + self.animation_duration_after:

                # only call on resume if it exists. It is like setup
                if hasattr(self.destination_view, 'on_resume_after_flip'):
                    self.destination_view.on_resume_after_flip()

                # move to new view
                self.window.show_view(self.destination_view)
