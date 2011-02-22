
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = (200,200)
        s.do(
            MoveTo((400,300), secs=1)
            )

Display.init((800,600), title="MoveTo Test")
Director.run(TestScene)
