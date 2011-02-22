
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s1 = TestSprite()
        s1.set(
            position = (100,100),
            velocity = (200,0),
            )
        s2 = TestSprite()
        s2.position = 400,300
        s2.do(KeepFacing(s1, offset=-90))
        

Display.init((800,600), title="KeepFacing Test")
Director.run(TestScene)
