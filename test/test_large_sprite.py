
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
            #alpha = 0,
            )
        #s.do(AlphaFade(1.0, secs=1))

Display.init((800,600), title="Large Sprite Test")
Director.run(TestScene)
