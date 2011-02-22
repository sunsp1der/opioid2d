
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = 400,300

        s1 = TestSprite()
        s1.position = 500, 300
        s1.do(OrbitAround(s, speed=50, align=False))

        s2 = TestSprite()
        s2.position = 400,100
        s2.rotation = -90
        s2.do(OrbitAround(s, speed=-25, align=True))
        

Display.init((800,600), title="OrbitAround Test")
Director.run(TestScene)
