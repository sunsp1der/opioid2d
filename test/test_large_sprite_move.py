
from Opioid2D import *

class TestImage(Image):
    filename = "opilarge.png"
    border = 1

class TestSprite(Sprite):
    image = TestImage
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.set(
            position = (100,300),
            #alpha = 0,
            )
        s.do(
            MoveDelta((600,0), secs=4, mode=PingPongMode)
            )

Display.init((800,600), title="Large Sprite Move Test")
Director.run(TestScene)
