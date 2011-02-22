
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.set(
            position = (400,300),
            alpha = 0,
            )
        s.do(
            Delay(0.5) + AlphaFade(1.0, secs=1) + MoveDelta((100,0), secs=0.5) + AlphaFade(0, secs=2)
            )

Display.init((800,600), title="AlphaFade Test")
Director.run(TestScene)
