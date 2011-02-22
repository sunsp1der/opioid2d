
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = 400,300
        act = Move((100,0)).limit(time=1) + \
              Fork(
                  ColorFade((0,0,1), secs=1),
                  Scale(2).limit(1),
                  ) + \
              Move((0,100))
        act.do(s)

Display.init((800,600), title="Action Test")
Director.run(TestScene)
