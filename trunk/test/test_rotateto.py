
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
            rotation = -130
            )
        s.do(
            RotateTo(80, secs=2, mode=StopMode)
            )

        s = TestSprite()
        s.set(
            position = (500,300),
            )
        s.do(
            RotateTo(300, speed=30, mode=StopMode)
            )

Display.init((800,600), title="RotateTo Test")
Director.run(TestScene)
