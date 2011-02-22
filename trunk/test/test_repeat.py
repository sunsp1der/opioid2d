
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = 100,100
        act = Repeat(
            MoveDelta((50,0),secs=1) + MoveDelta((0,50),secs=1)
            )
        act.do(s)

        s = TestSprite()
        s.position = 100,200
        act = Repeat(
            MoveDelta((50,0),secs=1) + MoveDelta((0,50),secs=1),
            repeats = 3
            )
        act.do(s)


Display.init((800,600), title="Action Test")
Director.run(TestScene)
