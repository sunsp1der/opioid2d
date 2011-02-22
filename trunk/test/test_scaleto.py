
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite('opilarge.png')
        s.position = (400,300)
        s.do(Delay(5) + ScaleTo(1.1, 2, mode=PingPongMode))
        
        s = TestSprite()
        s.set(
            position = (300,300),
            scale = 10,
            )
        s.do(
            ScaleTo(1, 2)
            )

        s = TestSprite()
        s.set(
            position = (500,300),
            scale = 10,
            )
        s.do(
            ScaleTo(-5, 5)
            )

Display.init((800,600), title="ScaleTo Test")
Director.run(TestScene)
