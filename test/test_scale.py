
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.set(
            position = (300,300),
            scale = 10,
            )
        s.do(
            Scale(-1, multiply=False)
            )

        s = TestSprite()
        s.set(
            position = (500,300),
            scale = 10,
            )
        s.do(
            Scale(0.9, multiply=True)
            )

Display.init((800,600), title="Action Test")
Director.run(TestScene)
