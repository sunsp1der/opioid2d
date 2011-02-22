
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
            )
        s.do(
            Delay(1) + SetAttr(velocity=(100,0))
            )

Display.init((800,600), title="Action Test")
Director.run(TestScene)
