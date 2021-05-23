import arcade
from arcade import Texture, Color

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_FLIP_ANIMATION_DURATION
from src.utils import bezier


class FlipAnimationView(arcade.View):

    def __init__(self, backgroundColor: Color, destination_view: arcade.View, animation_duration_after: float = .5):
        super().__init__()
        self.background_color = backgroundColor
        self.destination_view = destination_view
        self.animation_duration_after = animation_duration_after

        self.angle = 0
        self.animation_time = 0
        self.load_animation = True
        self.show_animation = False
        self.my_texture: Texture = None

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(self.background_color)
        if self.show_animation:
            self.my_texture.draw_scaled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, angle=self.angle)

    def on_update(self, delta_time: float):
        if self.load_animation:
            image = arcade.get_image()
            self.my_texture = Texture("Background", image)
            self.load_animation = False
            self.show_animation = True
            self.animation_time = 0
        elif self.show_animation:
            self.animation_time += delta_time
            if self.animation_time < WINDOW_FLIP_ANIMATION_DURATION:
                self.angle = 180 * bezier(self.animation_time / WINDOW_FLIP_ANIMATION_DURATION)
                if abs(self.angle - 180) < 2:
                    self.angle = 180
            elif self.animation_time > WINDOW_FLIP_ANIMATION_DURATION + self.animation_duration_after:
                if hasattr(self.destination_view, 'on_resume_after_flip'):
                    self.destination_view.on_resume_after_flip()
                self.window.show_view(self.destination_view)
