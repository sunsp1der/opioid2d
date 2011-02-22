
from Opioid2D import *

class TestSprite(Sprite):
    image = "opilarge.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.set(
            position = (400,300),
            rotation_speed = 50,
            scale = 1.5,
            )

Display.init((800,600), title="Large Sprite Rotate Test")
Director.run(TestScene)
