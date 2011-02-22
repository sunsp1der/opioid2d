
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
            RotateDelta(80, secs=1, mode=PingPongMode)
            )

        s = TestSprite()
        s.set(
            position = (500,300),
            )
        s.do(
            Rotate(100)
            )

Display.init((800,600), title="Action Test")
Director.run(TestScene)
