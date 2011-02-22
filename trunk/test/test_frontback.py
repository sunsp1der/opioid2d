
from Opioid2D import *

class LargeSprite(Sprite):
    image = "opilarge.png"
    layer = "sprite"

class SmallSprite(Sprite):
    image = "large_particle.png"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = LargeSprite()
        s.position = 400,300

        a = SmallSprite()
        a.position = -220,-100
        a.attach_to(s)

        b = SmallSprite()
        b.position = 220,100
        b.attach_to(s, back=True)
        

Display.init((800,600), title="Front/Back Child Test")
Director.run(TestScene)
