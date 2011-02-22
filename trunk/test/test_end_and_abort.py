
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
        act = Move((100,0)) + Move((0,100))
        act = act.do(s)
        (Delay(1) + CallFunc(act.end)).do()

        s = TestSprite()
        s.set(
            position = (200,100),
            )
        act = Move((100,0)) + Move((0,100))
        act = act.do(s)
        (Delay(1) + CallFunc(act.abort)).do()
        

Display.init((800,600), title="End/Abort Test")
Director.run(TestScene)
