
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"

class TestScene(Scene):
    layers = ["sprites"]

    def enter(self):
        n = Sprite()
        n.position = 50,50
        n.layer = "sprites"
        for y in range(10):
            for x in range(10):
                s = TestSprite()
                s.position = x*60, y*30
                s.attach_to(n)
                s.alpha = 0.2 + 0.8*(x*y)/100.0
                if (x+y) % 2:
                    s.color_inheritance = True
        n.do(
            Delay(1.0) + \
            ColorFade((1,0,0), secs=1.0) + \
            ColorFade((0,1,0), secs=1.0) + \
            ColorFade((0,0,1), secs=1.0) + \
            ColorFade((1,1,1), secs=1.0)
            )

Display.init((800,600), title="Color Inheritance Test")
Director.run(TestScene)
